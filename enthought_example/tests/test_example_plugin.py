import mock
import sys
import unittest

from force_bdss.app.bdss_application import BDSSApplication
try:
    # It's possible to install the example plugins in a headless system or
    # in a environment without wfmanager and the graphical stack for UIs.
    # Some tests will be skipped.
    from force_wfmanager.ui import BaseDataView, IDataView
    from force_wfmanager.ui import ContributedUI, IContributedUI
except ModuleNotFoundError:
    WFMANAGER_AVAILABLE = False
else:
    WFMANAGER_AVAILABLE = True

from enthought_example.example_plugin import ExamplePlugin
from enthought_example.tests import example_workflows


class TestExamplePlugin(unittest.TestCase):
    def test_basic_functionality(self):
        plugin = ExamplePlugin()
        self.assertEqual(1, len(plugin.data_source_factories))
        self.assertEqual(1, len(plugin.mco_factories))
        self.assertEqual(1, len(plugin.notification_listener_factories))
        self.assertEqual(1, len(plugin.ui_hooks_factories))

    @unittest.skipIf(
        not WFMANAGER_AVAILABLE,
        "No wfmanager found in the test environment. Skipping test.")
    def test_get_data_views(self):
        plugin = ExamplePlugin()
        plots = plugin.get_data_views()
        self.assertEqual(1, len(plots))
        for plot in plots:
            self.assertIsInstance(plot, type)
            self.assertTrue(issubclass(plot, BaseDataView))

    @unittest.skipIf(
        not WFMANAGER_AVAILABLE,
        "No wfmanager found in the test environment. Skipping test.")
    def test_get_contributed_uis(self):
        plugin = ExamplePlugin()
        custom_uis = plugin.get_contributed_uis()
        self.assertEqual(1, len(custom_uis))
        for custom_ui in custom_uis:
            self.assertIsInstance(custom_ui, type)
            self.assertTrue(issubclass(custom_ui, ContributedUI))

    @unittest.skipIf(
        not WFMANAGER_AVAILABLE,
        "No wfmanager found in the test environment. Skipping test.")
    def test_get_service_offer_factories(self):
        plugin = ExamplePlugin()
        service_offer_factories = plugin.get_service_offer_factories()
        self.assertEqual(2, len(service_offer_factories))

        interface, factories = service_offer_factories[0]
        self.assertEqual(IContributedUI, interface)
        interface, factories = service_offer_factories[1]
        self.assertEqual(IDataView, interface)


class TestExamplePluginIntegration(unittest.TestCase):

    def setUp(self):
        self.empty_workflow_path = example_workflows.get("empty_workflow.json")

    def test_plugins_imported(self):
        with mock.patch(
            "enthought_example.example_plugin.ExamplePlugin.get_name",
            side_effect=lambda: "Example"
        ) as mock_example_plugin_get_name:
            # initialize the command line app
            BDSSApplication(True, self.empty_workflow_path)
            mock_example_plugin_get_name.assert_called_once()

    def test_data_views_module_not_imported_by_bdss(self):
        # hide the example_data_views module
        sys.modules[
            "enthought_example.example_data_views.example_data_view"
        ] = None

        plugin = ExamplePlugin()
        # accessing get_data_view should trigger the import (and fail)
        with self.assertRaises(ModuleNotFoundError):
            plugin.get_data_views()

        # However, BDSS shouldn't attempt the import
        try:
            BDSSApplication(True, self.empty_workflow_path)
        except ModuleNotFoundError:
            self.fail("Has BDSS attempted to import .example_data_views?")

    def test_contributed_ui_module_not_imported_by_bdss(self):
        # hide the get_contributed_uis module
        sys.modules[
            "enthought_example.example_contributed_ui.example_contributed_ui"
        ] = None

        plugin = ExamplePlugin()
        # accessing get_contributed_uis should trigger the import (and fail)
        with self.assertRaises(ModuleNotFoundError):
            plugin.get_contributed_uis()

        # However, BDSS shouldn't attempt the import
        try:
            BDSSApplication(True, self.empty_workflow_path)
        except ModuleNotFoundError:
            self.fail("Has BDSS attempted to import .example_contributed_ui?")
