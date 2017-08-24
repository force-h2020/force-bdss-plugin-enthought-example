import unittest


try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.api import DataValue

from enthought_example.example_kpi_calculator.example_kpi_calculator import (
    ExampleKPICalculator
)
from enthought_example.example_kpi_calculator.example_kpi_calculator_model \
    import ExampleKPICalculatorModel
from enthought_example.example_kpi_calculator.example_kpi_calculator_factory \
    import ExampleKPICalculatorFactory


class TestExampleKPICalculator(unittest.TestCase):
    def test_basic_functionality(self):
        mock_factory = mock.Mock(ExampleKPICalculatorFactory)
        kpic = ExampleKPICalculator(mock_factory)
        model = ExampleKPICalculatorModel(mock_factory)
        model.cuba_type_in = "VALUE"
        model.cuba_type_out = "VALUE"
        dv1 = DataValue(type="PRESSURE", value=10)
        dv2 = DataValue(type="PRESSURE", value=30)

        # Note, we don't check types yet. This is a reminder that we do so.
        dv3 = DataValue(type="VOLUME", value=100)
        res = kpic.run(model, [dv1, dv2, dv3])
        self.assertEqual(res[0].type, "VALUE")
        self.assertEqual(res[0].value, 140)

    def test_slots(self):
        mock_factory = mock.Mock(ExampleKPICalculatorFactory)
        kpic = ExampleKPICalculator(mock_factory)
        model = ExampleKPICalculatorModel(mock_factory)
        in_slot, out_slot = kpic.slots(model)
        self.assertEqual(len(in_slot), 3)
        self.assertEqual(len(out_slot), 1)
