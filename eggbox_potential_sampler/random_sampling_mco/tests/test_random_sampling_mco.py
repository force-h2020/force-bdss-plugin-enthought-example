import unittest

from unittest import mock

from envisage.plugin import Plugin
from force_bdss.api import DataValue, Workflow
from force_bdss.app.workflow_file import WorkflowFile

from eggbox_potential_sampler.random_sampling_mco.parameters import (
    DummyMCOParameter, DummyMCOParameterFactory)

from eggbox_potential_sampler.random_sampling_mco.mco import (
    RandomSamplingMCO)
from eggbox_potential_sampler.random_sampling_mco.mco_factory import (
    RandomSamplingMCOFactory)


def probe_execute(*args, **kwargs):
    return [DataValue(value=1), DataValue(value=2)]


class TestRandomSamplingMCO(unittest.TestCase):
    def setUp(self):
        self.plugin = mock.Mock(spec=Plugin, id="pid")
        self.factory = RandomSamplingMCOFactory(self.plugin)
        self.factory.plugin.application = mock.Mock()
        self.factory.plugin.application.workflow_file = mock.Mock(
            spec=WorkflowFile, path="whatever",
            workflow=Workflow()
        )

    def test_initialization(self):
        opt = RandomSamplingMCO(self.factory)
        self.assertEqual(opt.factory, self.factory)

    def test_subprocess_run(self):
        opt = self.factory.create_optimizer()
        model = self.factory.create_model()
        model.num_trials = 7
        model.evaluation_mode = 'Subprocess'
        model.parameters = [DummyMCOParameter(
            mock.Mock(spec=DummyMCOParameterFactory))]

        mock_process = mock.Mock()
        mock_process.communicate = mock.Mock(return_value=(b"2", b"1 0"))

        with mock.patch("subprocess.Popen") as mock_popen:
            mock_popen.return_value = mock_process
            opt.run(model)

        self.assertEqual(mock_popen.call_count, 7)

    def test_internal_run(self):
        opt = self.factory.create_optimizer()
        model = self.factory.create_model()
        model.num_trials = 7
        model.evaluation_mode = 'Internal'
        model.parameters = [DummyMCOParameter(
            mock.Mock(spec=DummyMCOParameterFactory))]

        with mock.patch('force_bdss.api.Workflow.execute') as mock_exec:
            mock_exec.return_value = [DataValue(value=1), DataValue(value=2)]
            opt.run(model)
            self.assertEqual(mock_exec.call_count, 7)
