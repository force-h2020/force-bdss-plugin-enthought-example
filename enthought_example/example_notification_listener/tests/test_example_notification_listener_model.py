import unittest

from unittest import mock

from enthought_example.example_notification_listener\
     .example_notification_listener_factory import (
            ExampleNotificationListenerFactory)

from enthought_example.example_notification_listener\
    .example_notification_listener_model import (
        ExampleNotificationListenerModel)


class TestExampleNotificationListenerModel(unittest.TestCase):
    def test_initialization(self):
        factory = mock.Mock(spec=ExampleNotificationListenerFactory)
        model = ExampleNotificationListenerModel(factory)
        self.assertEqual(model.factory, factory)
