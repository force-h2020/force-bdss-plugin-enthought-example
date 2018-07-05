import unittest

try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.api import DataValue, Slot, BaseDataSourceFactory

from enthought_example.example_data_source.example_data_source import (
    ExampleDataSource
)
from enthought_example.example_data_source.example_data_source_model import (
    ExampleDataSourceModel
)


class TestPowerEvaluatorDataSource(unittest.TestCase):
    def setUp(self):
        self.factory = mock.Mock(spec=BaseDataSourceFactory)

    def test_initialization(self):
        ds = ExampleDataSource(self.factory)
        self.assertEqual(ds.factory, self.factory)

    def test_run(self):
        ds = ExampleDataSource(self.factory)
        model = ExampleDataSourceModel(self.factory)
        model.power = 2
        mock_params = [DataValue(value=5, type="METER")]
        result = ds.run(model, mock_params)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], DataValue)
        self.assertEqual(result[0].value, 25)

    def test_run_with_exception(self):
        ds = ExampleDataSource(self.factory)
        model = ExampleDataSourceModel(self.factory)
        mock_params = []
        model.power = 3
        with self.assertRaises(IndexError):
            ds.run(model, mock_params)

    def test_slots(self):
        ds = ExampleDataSource(self.factory)
        model = ExampleDataSourceModel(self.factory)
        slots = ds.slots(model)
        self.assertEqual(len(slots), 2)
        self.assertEqual(len(slots[0]), 1)
        self.assertEqual(len(slots[1]), 1)
        self.assertIsInstance(slots[0][0], Slot)
        self.assertIsInstance(slots[1][0], Slot)

        model.cuba_type_in = 'METER'
        model.cuba_type_out = 'METER'
        slots = ds.slots(model)
        self.assertEqual(slots[0][0].type, 'METER')
        self.assertEqual(slots[1][0].type, 'METER')
