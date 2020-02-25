import unittest

from traitsui.api import Group

try:
    # It's possible to install the example plugins in a headless system or
    # in a environment without wfmanager and the graphical stack for UIs.
    #
    # This module depends on UIs so won't be tested in this case.
    from enthought_example.example_contributed_ui\
        .example_contributed_ui import ExampleContributedUI
except ModuleNotFoundError:
    raise unittest.SkipTest(
        "No wfmanager found in the test environment. "
        "Contributed UIs can't be tested."
    )


class TestExampleContributedUI(unittest.TestCase):

    def setUp(self):
        self.custom_ui = ExampleContributedUI()

    def test___init__(self):

        self.assertIsNotNone(self.custom_ui.workflow_data)
        self.assertIsNotNone(self.custom_ui.workflow_group)
        self.assertIsInstance(self.custom_ui.workflow_group, Group)
        self.assertEqual(5, self.custom_ui.initial_value)

    def test_initial_value(self):
        self.custom_ui.lower = 0
        self.assertEqual(4.5, self.custom_ui.initial_value)
        self.custom_ui.upper = 10
        self.assertEqual(5, self.custom_ui.initial_value)

    def test_mco_data(self):

        mco_data = self.custom_ui._mco_data()
        keys = list(mco_data.keys())

        self.assertListEqual(['id', 'model_data'], keys)

    def test_execution_layer_data(self):

        execution_layer_data = self.custom_ui._execution_layer_data()
        self.assertEqual(2, len(execution_layer_data))

        for execution_layer in execution_layer_data:
            for data_source in execution_layer['data_sources']:
                keys = list(data_source.keys())
                self.assertListEqual(['id', 'model_data'], keys)

    def test_notification_listener_data(self):

        notification_listener_data = (
            self.custom_ui._notification_listener_data()
        )
        self.assertEqual(1, len(notification_listener_data))

        keys = list(notification_listener_data[0].keys())
        self.assertListEqual(['id', 'model_data'], keys)
