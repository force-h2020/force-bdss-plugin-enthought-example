import unittest

from enthought_example.example_plugin import ExamplePlugin


class TestExampleNotificationListenerFactory(unittest.TestCase):
    def setUp(self):
        self.plugin = ExamplePlugin()
        self.factory = self.plugin.notification_listener_factories[0]

    def test_create_methods(self):
        model = self.factory.create_model()
        self.assertEqual(model.factory, self.factory)

        model = self.factory.create_model({})
        self.assertEqual(model.factory, self.factory)

        listener = self.factory.create_listener()
        self.assertEqual(listener.factory, self.factory)
