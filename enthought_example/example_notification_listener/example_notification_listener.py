from __future__ import print_function

from force_bdss.api import (
    BaseNotificationListener,
    MCOStartEvent,
    MCOFinishEvent,
    MCOProgressEvent
)


class ExampleNotificationListener(BaseNotificationListener):
    """The notification listener will receive events as provided
    by the force_bdss API.
    At the moment, the following events are reported:

    MCOStartEvent: Emitted when the MCO has just started.
    MCOProgressEvent: Emitted when the MCO has generated
    a point that is a relevant result worth of output.
    MCOFinishEvent: Emitted when the MCO has concluded its
    execution.
    """

    #: This method must be reimplemented.
    #: It is called with an event as an argument.
    #: This implementation just prints the name of the event class.
    #: and its contents (if available). Each event carries a specific
    #: payload that can be extracted.
    def deliver(self, event):
        if isinstance(event, MCOStartEvent):
            print(event.__class__.__name__,
                  event.input_names,
                  event.output_names)
        elif isinstance(event, MCOProgressEvent):
            print(event.__class__.__name__,
                  event.input,
                  event.output)
        elif isinstance(event, MCOFinishEvent):
            print(event.__class__.__name__)
        else:
            print(event.__class__.__name__)

    #: You are not required to override these methods.
    #: They are executing when the BDSS starts up (or ends) and can be
    #: used to setup a database connection once and for all.
    def initialize(self, model):
        print("Initializing")

    def finalize(self):
        print("Finalizing")
