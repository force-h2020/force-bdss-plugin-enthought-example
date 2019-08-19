from force_bdss.api import plugin_id
from force_bdss.core_plugins.service_offers_plugin import ServiceOffersPlugin

from .example_notification_listener import ExampleNotificationListenerFactory
from .example_mco import ExampleMCOFactory
from .example_data_source import ExampleDataSourceFactory
from .example_ui_hooks import ExampleUIHooksFactory


PLUGIN_VERSION = 0


class ExamplePlugin(ServiceOffersPlugin):
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
            ExampleUIHooksFactory,
        ]

    # The following functionalities are optional (the plugin can be run on the
    # bdss without a GUI), so the quite expensive imports are done
    # inside eac method.
    def get_contributed_uis(self):
        """Get any ContributedUI classes included in the plugin"""
        from enthought_example.example_contributed_ui\
            .example_contributed_ui import ExampleContributedUI

        return [ExampleContributedUI]

    def get_data_views(self):
        """Get any BasePlot classes included in the plugin"""
        from enthought_example.example_data_views.example_data_view import \
            ExampleCustomPlot

        return [ExampleCustomPlot]

    def get_service_offer_factories(self):
        """Overloaded method of ServiceOffersPlugin class used to define service_offers
        trait"""
        from force_wfmanager.ui import IContributedUI
        from force_wfmanager.ui import IDataView

        contributed_uis = self.get_contributed_uis()
        data_views = self.get_data_views()

        return [
            (IContributedUI, contributed_uis),
            (IDataView, data_views)
        ]
