from force_bdss.api import BaseExtensionPlugin

from .example_notification_listener import ExampleNotificationListenerFactory
from .example_mco import ExampleMCOFactory
from .example_data_source import ExampleDataSourceFactory
from .example_ui_hooks import ExampleUIHooksFactory


class ExamplePlugin(BaseExtensionPlugin):
    """This is an example of the plugin system for the BDSS.
    This class provides access points for the various entities
    that the plugin system supports:

    - data sources: entities that perform calculations or
      retrieve data from external sources
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
    #: Define your organization unique identifier.
    def get_producer(self):
        return "enthought"

    #: Define a unique string of your liking. Make sure that
    #: is not reused by any of your other plugins. You are fully
    #: responsible for the uniqueness of this second string.
    def get_identifier(self):
        return "example"

    #: Define the factory classes that you want to export to this list.
    def get_factory_classes(self):
        return [
            ExampleDataSourceFactory,
            ExampleMCOFactory,
            ExampleNotificationListenerFactory,
            ExampleUIHooksFactory
        ]

