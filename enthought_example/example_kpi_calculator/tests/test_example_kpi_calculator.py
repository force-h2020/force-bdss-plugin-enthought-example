import unittest


try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.api import DataValue, BaseKPICalculatorFactory

from enthought_example.example_kpi_calculator.example_kpi_calculator import (
    ExampleKPICalculator
)
from enthought_example.example_kpi_calculator.example_kpi_calculator_model \
    import ExampleKPICalculatorModel


class TestKPIAdderCalculator(unittest.TestCase):
    def test_basic_functionality(self):
        kpic = ExampleKPICalculator(mock.Mock(spec=BaseKPICalculatorFactory))
        model = ExampleKPICalculatorModel(
            mock.Mock(spec=BaseKPICalculatorFactory))
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
        kpic = ExampleKPICalculator(mock.Mock(spec=BaseKPICalculatorFactory))
        model = ExampleKPICalculatorModel(
            mock.Mock(spec=BaseKPICalculatorFactory))
        in_slot, out_slot = kpic.slots(model)
        self.assertEqual(len(in_slot), 3)
        self.assertEqual(len(out_slot), 1)
