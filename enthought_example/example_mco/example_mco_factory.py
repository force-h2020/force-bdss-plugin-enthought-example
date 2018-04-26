from traits.api import String
from force_bdss.api import factory_id, BaseMCOFactory

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
    id = String(factory_id("enthought", "example_mco"))

    name = "Example MCO"

    #: The model class to instantiate. For more flexible initialization,
    #: you can instead reimplement the create_model method.
    #: For example::
    #:
    #:     def create_model(self, model_data=None):
    #:         if model_data is None:
    #:             model_data = {}
    #:         return ExampleMCOModel(self, **model_data)
    model_class = ExampleMCOModel

    #: The optimizer class, which is the class handling the actual MCO
    #: process. For a more flexible initialization, you can instead override
    #: the create_optimizer method.
    #: For example::
    #:
    #:     def create_optimizer(self):
    #:        return ExampleMCO(self)
    optimizer_class = ExampleMCO

    #: The communicator class to instantiate. It is the class that does
    #: interfacing between the executing MCO and the external program this
    #: executing MCO spawns to compute a single evaluation.
    #: By design, this external program is the BDSS itself with the option
    #: --evaluate.
    #: For a more flexible initialization, you can reimplement the
    #: create_communicator method instead.
    #: For example::
    #:
    #:     def create_communicator(self):
    #:         return ExampleMCOCommunicator(self)
    communicator_class = ExampleMCOCommunicator

    #: This method must return a list of all the possible
    #: parameter factories. This depends on what kind of parameters
    #: the MCO supports. For example, Dakota supports a parameter that is a
    #: range between two values (min/max)
    def parameter_factories(self):
        return [
            RangedMCOParameterFactory(self)
        ]
