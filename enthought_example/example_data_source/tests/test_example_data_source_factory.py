import unittest

from enthought_example.tests.data_source_factory_test_mixin import (
    DataSourceFactoryTestMixin)

from enthought_example.example_data_source.example_data_source import (
    ExampleDataSource
)
from enthought_example.example_data_source.example_data_source_model import (
    ExampleDataSourceModel
)
from enthought_example.example_data_source.example_data_source_factory import (
    ExampleDataSourceFactory
)


class TestExampleDataSourceFactory(DataSourceFactoryTestMixin,
                                   unittest.TestCase):
    @property
    def factory_class(self):
        return ExampleDataSourceFactory

    @property
    def model_class(self):
        return ExampleDataSourceModel

    @property
    def data_source_class(self):
        return ExampleDataSource
