import unittest

from unittest import mock

from force_bdss.api import BaseMCOFactory, DataValue, Workflow
from force_bdss.core.workflow_solver import WorkflowSolver

from eggbox_potential_sampler.random_sampling_mco.parameters import (
    DummyMCOParameter, DummyMCOParameterFactory)

from eggbox_potential_sampler.random_sampling_mco.mco_model import (
    RandomSamplingMCOModel)
from eggbox_potential_sampler.random_sampling_mco.mco import (
    RandomSamplingMCO)


class TestRandomSamplingMCO(unittest.TestCase):
    def setUp(self):
        self.factory = mock.Mock(spec=BaseMCOFactory)
        self.solver = WorkflowSolver(
            workflow=Workflow(),
            workflow_filepath="whatever"
        )

    def test_initialization(self):
        opt = RandomSamplingMCO(self.factory)
        self.assertEqual(opt.factory, self.factory)

    def test_subprocess_run(self):
        opt = RandomSamplingMCO(self.factory, )
        model = RandomSamplingMCOModel(self.factory)
        model.num_trials = 7
        model.evaluation_mode = 'Subprocess'
        model.parameters = [DummyMCOParameter(
            mock.Mock(spec=DummyMCOParameterFactory))]

        self.solver.workflow.mco = model

        mock_process = mock.Mock()
        mock_process.communicate = mock.Mock(return_value=(b"2", b"1 0"))
        with mock.patch("subprocess.Popen") as mock_popen:
            mock_popen.return_value = mock_process
            opt.run(model, self.solver)

        self.assertEqual(mock_popen.call_count, 7)

    def test_internal_run(self):
        opt = RandomSamplingMCO(self.factory, )
        model = RandomSamplingMCOModel(self.factory)
        model.num_trials = 7
        model.evaluation_mode = 'Internal'
        model.parameters = [DummyMCOParameter(
            mock.Mock(spec=DummyMCOParameterFactory))]

        self.solver.workflow.mco = model
        kpis = [DataValue(value=1), DataValue(value=2)]
        with mock.patch('force_bdss.api.Workflow.execute',
                        return_value=kpis) as mock_exec:
            opt.run(model, self.solver)
            self.assertEqual(mock_exec.call_count, 7)
