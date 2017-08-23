from force_bdss.api import BaseNotificationListenerModel


class ExampleNotificationListenerModel(BaseNotificationListenerModel):
    """
    This class contains the information needed by the notification listener.
    For example, if your notification listener is something that contacts
    a database, you would put here traits for the credentials and the URL
    to connect. The example listener does not need any configuration, so it's
    empty.

    Note: we don't yet have a UI in place to allow configuration
    of these parameters, nor to add notification listeners to your execution.
    For now, the only way for the BDSS to use notification listeners
    is to modify the workflow file by hand.
    """
    pass
