from force_bdss.api import BaseMCOFactory

# from force_bdss.core_plugins import BasicMCOCommunicator
from enthought_example.example_mco.example_mco_communicator import\
    ExampleMCOCommunicator
from .mco_model import ModelBasedOptimizationMCOModel
from .mco import ModelBasedOptimizationMCO
from .parameters import DummyMCOParameterFactory


class ModelBasedOptimizationMCOFactory(BaseMCOFactory):
    def get_identifier(self):
        return "model_based_mco"

    def get_name(self):
        return "Model-based MCO"

    #: Returns the model class
    def get_model_class(self):
        return ModelBasedOptimizationMCOModel

    #: Returns the optimizer class
    def get_optimizer_class(self):
        return ModelBasedOptimizationMCO

    #: Returns the communicator class
    def get_communicator_class(self):
        # return BasicMCOCommunicator
        return ExampleMCOCommunicator

    #: Factory classes of the parameters the MCO supports.
    def get_parameter_factory_classes(self):
        return [DummyMCOParameterFactory]
