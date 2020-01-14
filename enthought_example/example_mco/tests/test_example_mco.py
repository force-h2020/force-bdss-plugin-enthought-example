from unittest import mock, TestCase

from traits.api import TraitError

from force_bdss.api import Workflow, KPISpecification, WorkflowEvaluator

from enthought_example.example_mco.parameters import (
    RangedMCOParameter,
    RangedMCOParameterFactory,
)

from enthought_example.example_mco.example_mco import ExampleMCO
from enthought_example.example_mco.example_mco_factory import ExampleMCOFactory


class TestExampleMCO(TestCase):
    def setUp(self):
        self.plugin = {"id": "pid", "name": "Plugin"}
        self.factory = ExampleMCOFactory(self.plugin)
        self.evaluator = WorkflowEvaluator(
            workflow=Workflow(), workflow_filepath="whatever"
        )

    def test_initialization(self):
        opt = ExampleMCO(self.factory)
        self.assertEqual(opt.factory, self.factory)

    def test_run(self):
        opt = self.factory.create_optimizer()
        model = self.factory.create_model()
        model.parameters = [
            RangedMCOParameter(
                mock.Mock(spec=RangedMCOParameterFactory),
                lower_bound=1,
                upper_bound=3,
                initial_value=2,
            )
        ]
        model.kpis = [KPISpecification()]

        self.evaluator.workflow.mco_model = model
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
            RangedMCOParameter(
                mock.Mock(spec=RangedMCOParameterFactory), **model_data
            )
        ]

        mock_process = mock.Mock()
        mock_process.communicate = mock.Mock(return_value=(b"1 2 3", b""))

        with mock.patch("subprocess.Popen") as mock_popen:
            mock_popen.return_value = mock_process
            opt.run(self.evaluator)

        self.assertEqual(mock_popen.call_count, 2)

    def test_failure(self):
        model = self.factory.create_model()
        with self.assertRaises(TraitError):
            model.parameters = [
                RangedMCOParameter(
                    mock.Mock(spec=RangedMCOParameterFactory),
                    lower_bound=1,
                    upper_bound=3,
                    initial_value=5,
                )
            ]
