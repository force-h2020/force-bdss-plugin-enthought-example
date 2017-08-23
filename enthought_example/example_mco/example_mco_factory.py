from traits.api import String
from force_bdss.api import factory_id, BaseMCOFactory
from force_bdss.core_plugins.dummy.dummy_dakota.parameters import \
    RangedMCOParameterFactory

from .example_mco_communicator import DummyDakotaCommunicator
from .example_mco_model import DummyDakotaModel
from .example_mco import DummyDakotaOptimizer


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
    id = String(factory_id("enthought", "dummy_dakota"))

    name = "Dummy Dakota"

    def create_model(self, model_data=None):
        if model_data is None:
            model_data = {}
        return DummyDakotaModel(self, **model_data)

    def create_optimizer(self):
        return DummyDakotaOptimizer(self)

    #: This method creates the communicator. It is the class that does
    #: interfacing between the executing MCO and the external program this
    #: executing MCO spawns to compute a single evaluation.
    #: By design, this external program is the BDSS itself with the option
    #: --evaluate.
    def create_communicator(self):
        return DummyDakotaCommunicator(self)

    #: This method must return a list of all the possible
    #: parameter factories. This depends on what kind of parameters
    #: the MCO supports. For example, Dakota supports a parameter that is a
    #: range between two values (min/max)
    def parameter_factories(self):
        return [
            RangedMCOParameterFactory(self)
        ]
