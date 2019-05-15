import unittest

# from force_bdss.core_plugins import BasicMCOCommunicator
from enthought_example.example_mco.example_mco_communicator import \
    ExampleMCOCommunicator
from eggbox_potential_sampler.eggbox_plugin import EggboxPlugin
from eggbox_potential_sampler.model_based_mco.mco_model import (
    ModelBasedOptimizationMCOModel
)
from eggbox_potential_sampler.model_based_mco.mco import (
    ModelBasedOptimizationMCO
)


class TestModelBasedOptimizationMCOFactory(unittest.TestCase):
    def setUp(self):
        self.plugin = EggboxPlugin()
        self.factory = self.plugin.mco_factories[1]

    def test_initialization(self):
        self.assertIn("model_based_mco", self.factory.id)
        self.assertEqual(self.factory.plugin, self.plugin)

    def test_create_model(self):
        model = self.factory.create_model({})
        self.assertIsInstance(model, ModelBasedOptimizationMCOModel)

        model = self.factory.create_model()
        self.assertIsInstance(model, ModelBasedOptimizationMCOModel)

    def test_create_mco(self):
        ds = self.factory.create_optimizer()
        self.assertIsInstance(ds, ModelBasedOptimizationMCO)

    def test_create_communicator(self):
        ds = self.factory.create_communicator()
        # self.assertIsInstance(ds, BasicMCOCommunicator)
        self.assertIsInstance(ds, ExampleMCOCommunicator)

    def test_parameter_factories(self):
        self.assertNotEqual(len(self.factory.parameter_factories), 0)
