import unittest

from unittest import mock

from force_bdss.api import (
    DataValue, Workflow, KPISpecification
)


from eggbox_potential_sampler.random_sampling_mco.parameters import (
    DummyMCOParameter, DummyMCOParameterFactory)

from eggbox_potential_sampler.random_sampling_mco.mco import (
    RandomSamplingMCO
)
from eggbox_potential_sampler.random_sampling_mco.mco_factory import (
    RandomSamplingMCOFactory
)


class TestRandomSamplingMCO(unittest.TestCase):
    def setUp(self):
        self.plugin = {'id': 'pid', 'name': 'Plugin'}
        self.factory = RandomSamplingMCOFactory(self.plugin)
        self.evaluator = Workflow()

    def test_initialization(self):
        opt = RandomSamplingMCO(self.factory)
        self.assertEqual(opt.factory, self.factory)

    def test_subprocess_run(self):
        opt = self.factory.create_optimizer()
        model = self.factory.create_model()
        model.num_trials = 7
        model.evaluation_mode = 'Subprocess'
        parameter_factory = self.factory.parameter_factories[0]
        model.parameters = [DummyMCOParameter(parameter_factory)]
        model.kpis = [
            KPISpecification()
        ]

        self.evaluator.mco_model = model
        mock_process = mock.Mock()
        mock_process.communicate = mock.Mock(return_value=(b"2", b"1 0"))
        with mock.patch("subprocess.Popen") as mock_popen:
            mock_popen.return_value = mock_process
            opt.run(self.evaluator)

        self.assertEqual(mock_popen.call_count, 7)

    def test_internal_run(self):
        opt = self.factory.create_optimizer()
        model = self.factory.create_model()
        model.num_trials = 7
        model.evaluation_mode = 'Internal'
        parameter_factory = self.factory.parameter_factories[0]
        model.parameters = [DummyMCOParameter(parameter_factory)]
        model.kpis = [
            KPISpecification()
        ]

        self.evaluator.mco_model = model
        kpis = [DataValue(value=1), DataValue(value=2)]
        with mock.patch('force_bdss.api.Workflow.execute',
                        return_value=kpis) as mock_exec:
            opt.run(self.evaluator)
            self.assertEqual(mock_exec.call_count, 7)
