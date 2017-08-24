import unittest

from enthought_example.example_kpi_calculator.example_kpi_calculator import (
    ExampleKPICalculator
)
from enthought_example.example_kpi_calculator.example_kpi_calculator_model \
    import ExampleKPICalculatorModel
from enthought_example.example_kpi_calculator.example_kpi_calculator_factory \
    import ExampleKPICalculatorFactory

from enthought_example.tests.kpi_calculator_factory_test_mixin import (
    KPICalculatorFactoryTestMixin
)


class TestExampleKPICalculatorFactory(KPICalculatorFactoryTestMixin,
                                      unittest.TestCase):

    @property
    def factory_class(self):
        return ExampleKPICalculatorFactory

    @property
    def kpi_calculator_class(self):
        return ExampleKPICalculator

    @property
    def model_class(self):
        return ExampleKPICalculatorModel
