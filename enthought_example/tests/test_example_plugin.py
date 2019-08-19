import mock
import sys
import unittest

from force_bdss.bdss_application import BDSSApplication
try:
    # It's possible to install the example plugins in a headless system or
    # in a environment without wfmanager and the graphical stack for UIs.
    # Some tests will be skipped.
    from force_wfmanager.ui import BaseDataView
    from force_wfmanager.ui import ContributedUI
except ModuleNotFoundError:
    WFMANAGER_AVAILABLE = False
else:
    WFMANAGER_AVAILABLE = True

from enthought_example.example_plugin import ExamplePlugin
from enthought_example.tests import example_workflows


class TestExamplePlugin(unittest.TestCase):
    def test_basic_functionality(self):
        plugin = ExamplePlugin()
        self.assertEqual(len(plugin.data_source_factories), 1)
        self.assertEqual(len(plugin.mco_factories), 1)
        self.assertEqual(len(plugin.notification_listener_factories), 1)
        self.assertEqual(len(plugin.ui_hooks_factories), 1)

    @unittest.skipIf(
        not WFMANAGER_AVAILABLE,
        "No wfmanager found in the test environment. Skipping test.")
    def test_get_data_views(self):
        plugin = ExamplePlugin()
        plots = plugin.get_data_views()
        self.assertEqual(len(plots), 1)
        for plot in plots:
            self.assertIsInstance(plot, type)
            self.assertTrue(issubclass(plot, BaseDataView))

    @unittest.skipIf(
        not WFMANAGER_AVAILABLE,
        "No wfmanager found in the test environment. Skipping test.")
    def test_get_contributed_uis(self):
        plugin = ExamplePlugin()
        custom_uis = plugin.get_contributed_uis()
        self.assertEqual(len(custom_uis), 1)
        for custom_ui in custom_uis:
            self.assertIsInstance(custom_ui, type)
            self.assertTrue(issubclass(custom_ui, ContributedUI))


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
