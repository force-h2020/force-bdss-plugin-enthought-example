from force_bdss.api import plugin_id
from force_wfmanager.ui import UIExtensionPlugin

from .example_notification_listener import ExampleNotificationListenerFactory
from .example_mco import ExampleMCOFactory
from .example_data_source import ExampleDataSourceFactory
from .example_ui_hooks import ExampleUIHooksFactory
from .example_contributed_ui import ExampleContributedUI

PLUGIN_VERSION = 0


class ExamplePlugin(UIExtensionPlugin):
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
    #: Define the id of the plugin by calling the plugin_id function, and
    #: passing three information:
    #: - the producer: a unique string identifying the company or research
    #: institute.
    #: - the plugin identifier: a unique string identifying the plugin.
    #: - the version number of the plugin, as an integer.
    id = plugin_id("enthought", "example", PLUGIN_VERSION)

    def get_name(self):
        return "Enthought example"

    def get_description(self):
        return "An example plugin from Enthought"

    def get_version(self):
        return PLUGIN_VERSION

    #: Define the factory classes that you want to export to this list.
    def get_factory_classes(self):
        return [
            ExampleDataSourceFactory,
            ExampleMCOFactory,
            ExampleNotificationListenerFactory,
            ExampleUIHooksFactory
        ]

    def get_contributed_uis(self):
        return [
            ExampleContributedUI
        ]
