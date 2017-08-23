import math

from force_bdss.api import BaseDataSource, DataValue
from force_bdss.core.slot import Slot


class ExampleDataSource(BaseDataSource):
    """Defines an example data source.
    This data source specifically performs a power operation
    on its input.
    """

    #: This is where your computation happens.
    #: You receive the model, and a list of parameters
    #: that come from the MCO.
    #: Parameters are not plain numbers, but are instead instances
    #: of the DataValue class. This method must return a list
    #: of DataValue instances, whose number must match the number of
    #: output slots.
    def run(self, model, parameters):
        x = parameters[0].value
        return [
            DataValue(
                type=model.cuba_type_out,
                value=math.pow(x, model.power)
            )]

    #: If a data source is a function, the slots are the number of arguments
    #: it takes as input, and the number of entities it returns as output.
    #: This method must return a tuple of tuples. (input_tuple, output_tuple)
    #: Each tuple contains Slot instances. You can decide this information
    #: according to the model content, therefore if your data source returns
    #: different data depending on its settings, you can definitely handle
    #: this case.
    #: In this case, the data source is like a function
    #:
    #:                    a = pow(b)
    #:
    #: so it has one input slot and one output slot.
    #: a function like
    #:
    #:                a, b = func(m,n,o)
    #:
    #: has three input slots and two output slots.
    def slots(self, model):
        return (
            (
                Slot(type=model.cuba_type_in),
            ),
            (
                Slot(type=model.cuba_type_out),
            )
        )
