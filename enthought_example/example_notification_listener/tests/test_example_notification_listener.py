#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import unittest
from enthought_example.tests.utils import captured_output

from unittest import mock

from force_bdss.api import (
    MCOStartEvent, MCOProgressEvent, MCOFinishEvent, DataValue)


from enthought_example.example_notification_listener\
    .example_notification_listener_model import (
        ExampleNotificationListenerModel)
from enthought_example.example_notification_listener\
    .example_notification_listener_factory import (
        ExampleNotificationListenerFactory)
from enthought_example.example_notification_listener\
    .example_notification_listener import (
        ExampleNotificationListener)


class TestExampleNotificationListener(unittest.TestCase):
    def test_initialization(self):
        listener = ExampleNotificationListener(
            mock.Mock(spec=ExampleNotificationListenerFactory))
        model = mock.Mock(spec=ExampleNotificationListenerModel)
        with captured_output() as (out, err):
            listener.initialize(model)
            listener.deliver(MCOStartEvent(
                parameter_names=["foo", "bar"],
                kpi_names=["baz", "quux"]))
            listener.deliver(MCOProgressEvent(
                optimal_point=[DataValue(value=1.0), DataValue(value=2.0)],
                optimal_kpis=[DataValue(value=3.0), DataValue(value=4.0)]
            ))
            listener.deliver(MCOFinishEvent())
            listener.finalize()

        self.assertEqual(
            out.getvalue(),
            "Initializing\n"
            "MCOStartEvent ['foo', 'bar'] ['baz', 'quux']\n"
            "MCOProgressEvent [1.0, 2.0] [3.0, 4.0]\n"
            "MCOFinishEvent\n"
            "Finalizing\n"
        )
