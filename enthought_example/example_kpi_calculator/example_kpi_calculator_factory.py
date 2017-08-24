from traits.api import String

from force_bdss.api import factory_id, BaseKPICalculatorFactory

from .example_kpi_calculator_model import ExampleKPICalculatorModel
from .example_kpi_calculator import ExampleKPICalculator


class ExampleKPICalculatorFactory(BaseKPICalculatorFactory):
    """Refer to the data source example"""
    id = String(factory_id("enthought", "example_kpi_calculator"))

    name = String("Example KPI Calculator (Adder)")

    def create_model(self, model_data=None):
        if model_data is None:
            model_data = {}

        return ExampleKPICalculatorModel(self, **model_data)

    def create_kpi_calculator(self):
        return ExampleKPICalculator(self)
