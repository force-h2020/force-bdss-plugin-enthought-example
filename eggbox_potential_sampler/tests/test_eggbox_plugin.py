#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import mock
import sys
import unittest

from force_bdss.app.bdss_application import BDSSApplication
try:
    # It's possible to install the example plugins in a headless system or
    # in a environment without wfmanager and the graphical stack for UIs.
    # Some tests will be skipped.
    import force_wfmanager # noqa
except ModuleNotFoundError:
    WFMANAGER_AVAILABLE = False
else:
    from force_wfmanager.ui.review.base_data_view import BaseDataView
    WFMANAGER_AVAILABLE = True

from eggbox_potential_sampler.eggbox_plugin import EggboxPlugin
from enthought_example.tests import example_workflows


class TestEggboxPlugin(unittest.TestCase):

    def test_basic_functionality(self):
        plugin = EggboxPlugin()
        self.assertEqual(len(plugin.data_source_factories), 1)
        self.assertEqual(len(plugin.mco_factories), 1)
        self.assertEqual(len(plugin.notification_listener_factories), 0)
        self.assertEqual(len(plugin.ui_hooks_factories), 0)

    @unittest.skipIf(
        not WFMANAGER_AVAILABLE,
        "No wfmanager found in the test environment. Skipping test.")
    def test_get_data_views(self):
        plugin = EggboxPlugin()
        plots = plugin.get_data_views()
        self.assertEqual(len(plots), 1)
        for plot in plots:
            self.assertIsInstance(plot, type)
            self.assertTrue(issubclass(plot, BaseDataView))


class TestEggboxPluginIntegration(unittest.TestCase):

    def setUp(self):
        self.empty_workflow_path = example_workflows.get("empty_workflow.json")

    def test_plugins_imported(self):
        with mock.patch(
            "eggbox_potential_sampler.eggbox_plugin.EggboxPlugin.get_name",
            side_effect=lambda: "Example"
        ) as mock_example_plugin_get_name:
            # initialize the command line app
            BDSSApplication(True, self.empty_workflow_path)
            mock_example_plugin_get_name.assert_called_once()

    def test_data_views_module_not_imported_by_bdss(self):
        # hide the example_data_views module
        sys.modules[
            "eggbox_potential_sampler.sampling_data_view.sampling_data_view"
        ] = None

        plugin = EggboxPlugin()
        # accessing get_data_view should trigger the import (and fail)
        with self.assertRaises(ModuleNotFoundError):
            plugin.get_data_views()

        # However, BDSS shouldn't attempt the import
        try:
            BDSSApplication(True, self.empty_workflow_path)
        except ModuleNotFoundError:
            self.fail("Has BDSS attempted to import .example_data_views?")
