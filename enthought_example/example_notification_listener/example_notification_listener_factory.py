from traits.api import String

from force_bdss.api import (
    factory_id,
    BaseNotificationListenerFactory)

from .example_notification_listener import ExampleNotificationListener
from .example_notification_listener_model import \
    ExampleNotificationListenerModel


class ExampleNotificationListenerFactory(BaseNotificationListenerFactory):
    """This is the factory of the notification listener.
    A notification listener listens to events provided by the MCO,
    and performs operations accordingly.
    """

    #: For all the code following, see the documentation on the example
    #: data source for this
    id = String(factory_id("enthought", "example_notification_listener"))

    name = String("Example Notification Listener (stdout print)")

    #: You can specify the model class here. If you want to have a more complex
    #: model initialization, you can leave this variable unspecified, and
    #: override the create_model method instead.
    #: For example::
    #:
    #: def create_model(self, model_data=None):
    #:    if model_data is None:
    #:        model_data = {}
    #:
    #:    return ExampleNotificationListenerModel(self, **model_data)
    model_class = ExampleNotificationListenerModel

    #: The listener class to instantiate. For a more flexible initialization
    #: you can override the create_listener method instead.
    #: For example::
    #:
    #: def create_listener(self):
    #:    return ExampleNotificationListener(self)
    listener_class = ExampleNotificationListener
