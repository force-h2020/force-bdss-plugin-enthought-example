import unittest

# from force_bdss.core_plugins import BasicMCOCommunicator
from enthought_example.example_mco.example_mco_communicator import \
    ExampleMCOCommunicator
from eggbox_potential_sampler.eggbox_plugin import EggboxPlugin
from eggbox_potential_sampler.random_sampling_mco.mco_model import (
    RandomSamplingMCOModel
)
from eggbox_potential_sampler.random_sampling_mco.mco import RandomSamplingMCO


class TestRandomSamplingMCOFactory(unittest.TestCase):
    def setUp(self):
        self.plugin = EggboxPlugin()
        self.factory = self.plugin.mco_factories[0]

    def test_initialization(self):
        self.assertIn("random_sampling_mco", self.factory.id)
        self.assertEqual(self.factory.plugin_id, self.plugin.id)

    def test_create_model(self):
        model = self.factory.create_model({})
        self.assertIsInstance(model, RandomSamplingMCOModel)

        model = self.factory.create_model()
        self.assertIsInstance(model, RandomSamplingMCOModel)

    def test_create_mco(self):
        ds = self.factory.create_optimizer()
        self.assertIsInstance(ds, RandomSamplingMCO)

    def test_create_communicator(self):
        ds = self.factory.create_communicator()
        self.assertIsInstance(ds, ExampleMCOCommunicator)

    def test_parameter_factories(self):
        self.assertNotEqual(len(self.factory.parameter_factories), 0)
