from force_bdss.api import BaseKPICalculator, DataValue, Slot


class ExampleKPICalculator(BaseKPICalculator):
    """Refer to the Data Source example.

    This KPI calculator takes three values sums them together, and
    returns the sum.
    """
    def run(self, model, data_source_results):
        sum = 0.0

        for res in data_source_results:
            sum += res.value

        return [
            DataValue(
                type=model.cuba_type_out,
                value=sum
            )]

    def slots(self, model):
        return (
            (
                Slot(type=model.cuba_type_in),
                Slot(type=model.cuba_type_in),
                Slot(type=model.cuba_type_in),
            ),
            (
                Slot(type=model.cuba_type_out),
            )
        )
