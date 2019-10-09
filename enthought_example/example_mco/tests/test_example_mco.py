import unittest

from unittest import mock
from traits.api import TraitError

from force_bdss.api import BaseMCOFactory, Workflow
from force_bdss.app.workflow_evaluator import WorkflowEvaluator

from enthought_example.example_mco.parameters import (
    RangedMCOParameter,
    RangedMCOParameterFactory
)

from enthought_example.example_mco.example_mco_model import ExampleMCOModel
from enthought_example.example_mco.example_mco import (
    ExampleMCO, SubprocessWorkflowEvaluator
)


class TestExampleMCO(unittest.TestCase):
    def setUp(self):
        self.factory = mock.Mock(spec=BaseMCOFactory)
        self.evaluator = WorkflowEvaluator(
            workflow=Workflow(),
            workflow_filepath="whatever"
        )

    def test_initialization(self):
        opt = ExampleMCO(self.factory)
        self.assertEqual(opt.factory, self.factory)

    def test_run(self):
        opt = ExampleMCO(self.factory)
        model = ExampleMCOModel(self.factory)
        model.parameters = [
            RangedMCOParameter(
                mock.Mock(spec=RangedMCOParameterFactory),
                lower_bound=1,
                upper_bound=3,
                initial_value=2)
        ]

        self.evaluator.workflow.mco = model
        mock_process = mock.Mock()
        mock_process.communicate = mock.Mock(return_value=(b"1 2 3", b""))
        with mock.patch("subprocess.Popen") as mock_popen:
            mock_popen.return_value = mock_process
            opt.run(self.evaluator)

        self.assertEqual(mock_popen.call_count, 2)

        # test whether argument order matters on object creation
        model.parameters = [
            RangedMCOParameter(
                mock.Mock(spec=RangedMCOParameterFactory),
                initial_value=2,
                upper_bound=3,
                lower_bound=1,
            )
        ]

        mock_process = mock.Mock()
        mock_process.communicate = mock.Mock(return_value=(b"1 2 3", b""))

        with mock.patch("subprocess.Popen") as mock_popen:
            mock_popen.return_value = mock_process
            opt.run(self.evaluator)

        self.assertEqual(mock_popen.call_count, 2)

        # test whether argument order matters on object creation
        model_data = {"initial_value": 2, "upper_bound": 3, "lower_bound": 1}
        model.parameters = [
            RangedMCOParameter(mock.Mock(spec=RangedMCOParameterFactory),
                               **model_data)
        ]

        mock_process = mock.Mock()
        mock_process.communicate = mock.Mock(return_value=(b"1 2 3", b""))

        with mock.patch("subprocess.Popen") as mock_popen:
            mock_popen.return_value = mock_process
            opt.run(self.evaluator)

        self.assertEqual(mock_popen.call_count, 2)

    def test_failure(self):
        model = ExampleMCOModel(self.factory)
        with self.assertRaises(TraitError):
            model.parameters = [
                RangedMCOParameter(
                    mock.Mock(spec=RangedMCOParameterFactory),
                    lower_bound=1,
                    upper_bound=3,
                    initial_value=5,
                )
            ]


class TestSubprocessWorkflowEvaluator(unittest.TestCase):

    def setUp(self):

        self.evaluator = SubprocessWorkflowEvaluator(
            workflow=Workflow(),
            workflow_filepath="test_probe.json"
        )
        self.mock_process = mock.Mock()
        self.mock_process.communicate = mock.Mock(
            return_value=(b"2", b"1 0")
        )

    def test___call_subprocess(self):

        # Test simple bash command
        stdout = self.evaluator._call_subprocess(
            'uniq', ['Hello', 'World']
        )
        self.assertEqual(
            'Hello World', stdout.decode("utf-8").strip()
        )

    def test__subprocess_solve(self):
        factory = mock.Mock(spec=BaseMCOFactory)
        self.evaluator.workflow.mco = ExampleMCOModel(factory)

        with mock.patch("subprocess.Popen") as mock_popen:
            mock_popen.return_value = self.mock_process
            kpi_results = self.evaluator._subprocess_evaluate([1.0])

        self.assertEqual(1, len(kpi_results))

    def test_solve_error_mco_communicator(self):

        def mock_subprocess_evaluate(self, *args):
            raise Exception

        factory = mock.Mock(spec=BaseMCOFactory)
        self.evaluator.workflow.mco = ExampleMCOModel(factory)

        with mock.patch('enthought_example.example_mco.example_mco'
                        '.SubprocessWorkflowEvaluator._subprocess_evaluate',
                        side_effect=mock_subprocess_evaluate):
            with self.assertRaisesRegex(
                    RuntimeError,
                    'SubprocessWorkflowEvaluator failed '
                    'to run. This is likely due to an error in the '
                    'BaseMCOCommunicator assigned to '
                    "<class 'force_bdss.mco.base_mco_factory."
                    "BaseMCOFactory'>."):
                self.evaluator.evaluate([1.0])
