import unittest

from enthought_example.example_data_source.example_data_source import (
    ExampleDataSource
)
from enthought_example.example_data_source.example_data_source_model import (
    ExampleDataSourceModel
)
from enthought_example.example_plugin import ExamplePlugin


class DataSourceFactoryTestMixin(unittest.TestCase):
    def setUp(self):
        self.plugin = ExamplePlugin()
        self.factory = self.plugin.data_source_factories[0]

    def test_initialization(self):
        self.assertNotEqual(self.factory.id, "")
        self.assertEqual(self.factory.plugin_id, self.plugin.id)

    def test_create_model(self):
        model = self.factory.create_model({})
        self.assertIsInstance(model, ExampleDataSourceModel)

        model = self.factory.create_model()
        self.assertIsInstance(model, ExampleDataSourceModel)

    def test_create_data_source(self):
        ds = self.factory.create_data_source()
        self.assertIsInstance(ds, ExampleDataSource)
