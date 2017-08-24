from force_bdss.api import BaseExtensionPlugin, plugin_id

from .example_notification_listener import ExampleNotificationListenerFactory
from .example_mco import ExampleMCOFactory
from .example_data_source import ExampleDataSourceFactory
from .example_kpi_calculator import ExampleKPICalculatorFactory
from .example_ui_hooks import ExampleUIHooksFactory


class ExamplePlugin(BaseExtensionPlugin):
    """This is an example of the plugin system for the BDSS.
    This class provides access points for the various entities
    that the plugin system supports:

    - data sources: entities that perform calculations or
      retrieve data from external sources
    - KPI calculators: entities performing final evaluation of
      the KPIs. Note that this is probably going to disappear,
      and it will be replaced by data sources that can support
      marking of a returned value as a KPI.
    - MCO: multi criteria optimizer support. Note that the MCO
      must obey an execution model as in Dakota, that is,
      this plugin spawns the MCO, which spawns subprocesses
      performing the single-point evaluation.
    - Notification listeners: entities that handle notifications
      from the MCO as it computes data and can perform actions
      accordingly. The MCO plugin must trigger the appropriate
      events, otherwise no notification will be triggered.
      You can use notification listeners to submit data to a
      database as they are computed.
    - UI Hooks: provides hook methods that are called in some
      specific moments of the FORCE UI.
    """
    #: Define this id using the plugin_id function.
    #: The first parameter is your organization unique identifier.
    #: The second is a unique string of your liking. Make sure that
    #: is not reused by any of your other plugins. You are fully
    #: responsible for the uniqueness of this second string.
    id = plugin_id("enthought", "example")

    #: You define these methods to return a list of "factory"
    #: classes. You are free to implement only the methods that
    #: you need. If you are not exporting any data sources, for
    #: example the following method is not needed.
    def _data_source_factories_default(self):
        return [ExampleDataSourceFactory(self)]

    def _mco_factories_default(self):
        return [ExampleMCOFactory(self)]

    def _kpi_calculator_factories_default(self):
        return [ExampleKPICalculatorFactory(self)]

    def _notification_listener_factories_default(self):
        return [ExampleNotificationListenerFactory(self)]

    def _ui_hooks_factories_default(self):
        return [ExampleUIHooksFactory(self)]
