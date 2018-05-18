import unittest

from enthought_example.example_plugin import ExamplePlugin

from enthought_example.example_mco.example_mco_communicator import (
    ExampleMCOCommunicator
)
from enthought_example.example_mco.example_mco_model import (
    ExampleMCOModel
)
from enthought_example.example_mco.example_mco import ExampleMCO


class TestExampleMCOFactory(unittest.TestCase):
    def setUp(self):
        self.plugin = ExamplePlugin()
        self.factory = self.plugin.mco_factories[0]

    def test_initialization(self):
        self.assertIn("example_mco", self.factory.id)
        self.assertEqual(self.factory.plugin, self.plugin)

    def test_create_model(self):
        model = self.factory.create_model({})
        self.assertIsInstance(model, ExampleMCOModel)

        model = self.factory.create_model()
        self.assertIsInstance(model, ExampleMCOModel)

    def test_create_mco(self):
        ds = self.factory.create_optimizer()
        self.assertIsInstance(ds, ExampleMCO)

    def test_create_communicator(self):
        ds = self.factory.create_communicator()
        self.assertIsInstance(ds, ExampleMCOCommunicator)

    def test_parameter_factories(self):
        self.assertNotEqual(len(self.factory.parameter_factories()), 0)
