import unittest

from eggbox_potential_sampler.eggbox_plugin import EggboxPlugin


class TestExamplePlugin(unittest.TestCase):
    def test_basic_functionality(self):
        plugin = EggboxPlugin()
        self.assertEqual(len(plugin.data_source_factories), 1)
        self.assertEqual(len(plugin.mco_factories), 2)
        self.assertEqual(len(plugin.notification_listener_factories), 0)
        self.assertEqual(len(plugin.ui_hooks_factories), 0)
