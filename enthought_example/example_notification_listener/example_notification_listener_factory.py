from force_bdss.api import BaseNotificationListenerFactory

from .example_notification_listener import ExampleNotificationListener
from .example_notification_listener_model import \
    ExampleNotificationListenerModel


class ExampleNotificationListenerFactory(BaseNotificationListenerFactory):
    """This is the factory of the notification listener.
    A notification listener listens to events provided by the MCO,
    and performs operations accordingly.
    """

    #: Return a unique string identifier within the scope of your plugin for
    #: this factory
    def get_identifier(self):
        return "example_notification_listener"

    #: Return a user-visible name for the factory
    def get_name(self):
        return "Example Notification Listener (stdout print)"

    #: Return the model class associated to this factory.
    def get_model_class(self):
        return ExampleNotificationListenerModel

    #: Return the class of the notification listener.
    def get_listener_class(self):
        return ExampleNotificationListener
