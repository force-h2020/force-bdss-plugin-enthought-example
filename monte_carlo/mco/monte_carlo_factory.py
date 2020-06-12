#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from force_bdss.api import (
    BaseMCOFactory,
    BaseMCOCommunicator,
    FixedMCOParameterFactory,
    ListedMCOParameterFactory,
    RangedMCOParameterFactory,
    RangedVectorMCOParameterFactory,
    CategoricalMCOParameterFactory,
)

from .monte_carlo_model import MonteCarloModel
from .monte_carlo_mco import MonteCarloMCO


class MonteCarloFactory(BaseMCOFactory):
    """ Base MonteCarlo MCO Factory with generic configuration.
        Users might want to add custom MCOCommunicator instead of the
        BaseMCOCommunicator. Also, the parameter_factory method can
        be updated for custom MCOParameterFactories.
    """

    def get_identifier(self):
        return "monte_carlo_mco"

    def get_name(self):
        return "Monte Carlo sampling and optimization"

    #: Returns the model class
    def get_model_class(self):
        return MonteCarloModel

    #: Returns the optimizer class
    def get_optimizer_class(self):
        return MonteCarloMCO

    #: Returns the communicator class
    def get_communicator_class(self):
        return BaseMCOCommunicator

    #: Factory classes of the parameters the MCO supports.
    def get_parameter_factory_classes(self):
        return [
            FixedMCOParameterFactory,
            ListedMCOParameterFactory,
            RangedMCOParameterFactory,
            CategoricalMCOParameterFactory,
            RangedVectorMCOParameterFactory
        ]
