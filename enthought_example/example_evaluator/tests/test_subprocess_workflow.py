import testfixtures
from unittest import mock, TestCase

from force_bdss.api import BaseMCOFactory

from enthought_example.example_mco.example_mco_model import ExampleMCOModel
from enthought_example.example_mco.example_mco import (
    SubprocessWorkflow
)

WORKFLOW_GETSTATE_PATH = 'force_bdss.core.workflow.Workflow.__getstate__'


def mock_workflow_getstate():
    """Mocks the Workflow.__getstate__ method to include
     BaseNotificationListener instances"""
    return {
        "mco_model": None,
        "execution_layers": [],
        "notification_listeners": [
            {"id": "force.bdss.enthought.plugin.some_listener.v0"
                   ".factory.some_listener",
             "model_data": {}},
            {"id":  "force.bdss.enthought.plugin.ui_notification.v0"
                    ".factory.ui_notification",
             "model_data":  {}}
        ]
    }


class TestSubprocessWorkflow(TestCase):

    def setUp(self):
        self.evaluator = SubprocessWorkflow(
            workflow_filepath="test_probe.json")
        self.mock_process = mock.Mock()
        self.mock_process.communicate = mock.Mock(
            return_value=(b"2", b"1 0"))

    def test_getstate(self):
        with mock.patch(WORKFLOW_GETSTATE_PATH) as mock_getstate:
            mock_getstate.side_effect = mock_workflow_getstate
            self.assertDictEqual(
                {"mco_model": None,
                 "execution_layers": [],
                 "notification_listeners": []},
                self.evaluator.__getstate__())

    def test___call_subprocess(self):

        # Test simple bash command
        stdout = self.evaluator._call_subprocess(["uniq"], ["Hello", "World"])
        self.assertEqual("Hello World", stdout.decode("utf-8").strip())

    def test__subprocess_solve(self):
        factory = mock.Mock(spec=BaseMCOFactory)
        self.evaluator.mco_model = ExampleMCOModel(factory)

        with mock.patch("subprocess.Popen") as mock_popen:
            mock_popen.return_value = self.mock_process
            kpi_results = self.evaluator._subprocess_evaluate([
                1.0], 'dummy_filename')

        self.assertEqual(1, len(kpi_results))

    def test_solve_error_mco_communicator(self):
        def mock_subprocess_evaluate(self, *args):
            raise Exception

        factory = mock.Mock(spec=BaseMCOFactory)
        self.evaluator.mco_model = ExampleMCOModel(factory)

        with mock.patch('enthought_example.example_mco.example_mco'
                        '.SubprocessWorkflow._subprocess_evaluate',
                        side_effect=mock_subprocess_evaluate):
            with testfixtures.LogCapture():
                with self.assertRaisesRegex(
                        RuntimeError,
                        'SubprocessWorkflow failed '
                        'to run. This is likely due to an error in the '
                        'BaseMCOCommunicator assigned to '
                        "<class 'force_bdss.mco.base_mco_factory."
                        "BaseMCOFactory'>."):
                    self.evaluator.evaluate([1.0])
