import unittest

from enthought_example.example_plugin import ExamplePlugin


class TestExamplePlugin(unittest.TestCase):
    def test_basic_functionality(self):
        plugin = ExamplePlugin()
        self.assertEqual(len(plugin.data_source_factories), 1)
        self.assertEqual(len(plugin.mco_factories), 1)
        self.assertEqual(len(plugin.notification_listener_factories), 1)
        self.assertEqual(len(plugin.ui_hooks_factories), 1)
