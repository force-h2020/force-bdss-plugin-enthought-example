import unittest

from envisage.plugin import Plugin

try:
    import mock
except ImportError:
    from unittest import mock

from enthought_example.example_notification_listener \
    .example_notification_listener_factory import (
        ExampleNotificationListenerFactory)


class TestExampleNotificationListenerFactory(unittest.TestCase):
    def test_create_methods(self):
        factory = ExampleNotificationListenerFactory(mock.Mock(spec=Plugin))
        model = factory.create_model()
        self.assertEqual(model.factory, factory)

        model = factory.create_model({})
        self.assertEqual(model.factory, factory)

        listener = factory.create_listener()
        self.assertEqual(listener.factory, factory)
