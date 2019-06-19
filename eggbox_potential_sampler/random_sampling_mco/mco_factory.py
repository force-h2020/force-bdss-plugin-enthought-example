from force_bdss.api import BaseMCOFactory

from enthought_example.example_mco.example_mco_communicator import (
    ExampleMCOCommunicator
)
from .mco_model import RandomSamplingMCOModel
from .mco import RandomSamplingMCO
from .parameters import DummyMCOParameterFactory


class RandomSamplingMCOFactory(BaseMCOFactory):
    def get_identifier(self):
        return "random_sampling_mco"

    def get_name(self):
        return "Random sampling MCO"

    #: Returns the model class
    def get_model_class(self):
        return RandomSamplingMCOModel

    #: Returns the optimizer class
    def get_optimizer_class(self):
        return RandomSamplingMCO

    #: Returns the communicator class
    def get_communicator_class(self):
        return ExampleMCOCommunicator

    #: Factory classes of the parameters the MCO supports.
    def get_parameter_factory_classes(self):
        return [DummyMCOParameterFactory]
