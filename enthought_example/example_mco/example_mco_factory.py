from force_bdss.api import BaseMCOFactory

from .example_mco_communicator import ExampleMCOCommunicator
from .example_mco_model import ExampleMCOModel
from .example_mco import ExampleMCO
from .parameters import RangedMCOParameterFactory


class ExampleMCOFactory(BaseMCOFactory):
    """An MCO factory is responsible for creating the objects
    relative to the MCOs.

    An MCO execution model is assumed to be as in Dakota.
    Dakota works as follows: it reads an input file containing the details of
    what to be carried out.
    specifically, it contains which parameters it is supposed to generate,
    which KPIs are obtained, and where is (path) the external program
    performing the transformation between a selection of the parameters
    and the resulting KPIs.

    This execution model is required for our system. Any other MCO that needs
    to be integrated in our system must support it.

    For the above reasons, the following classes are required:

    - A MCO, which is the core orchestrator of spawning the initial
      MCO executable, parsing its output and emitting events as the
      calculation progresses.
    - a MCO Model, which contains general configuration options of the MCO.
    - a set of MCO parameters that the MCO supports, which are specifications
      of which parameters the MCO should generate, according to some
      constraints.
    - A communicator, that is responsible to format the data in transit
      between the MCO executable (e.g. the dakota program) and the executable
      it spawns to compute a single evaluation.
    - and finally a Factory (this class) that is responsible for generating
      all of the above.
    """
    #: See notes on Data Source Factory for everything not described.
    def get_identifier(self):
        return "example_mco"

    #: Returns a user visible name for the factory.
    def get_name(self):
        return "Example MCO"

    #: Returns a description of what the MCO does.
    def get_description(self):
        return (
            "An example \"MCO\" which does not actually do any optimising!"
        )

    #: Returns the model class
    def get_model_class(self):
        return ExampleMCOModel

    #: Returns the optimizer class
    def get_optimizer_class(self):
        return ExampleMCO

    #: Returns the communicator class
    def get_communicator_class(self):
        return ExampleMCOCommunicator

    #: This method must return a list of all the possible parameter factory
    #: classes. This depends on what kind of parameters the MCO supports.
    def get_parameter_factory_classes(self):
        return [
            RangedMCOParameterFactory
        ]
