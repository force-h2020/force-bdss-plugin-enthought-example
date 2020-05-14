#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import unittest

from enthought_example.example_plugin import ExamplePlugin
from enthought_example.example_ui_hooks.example_ui_hooks_manager import (
    ExampleUIHooksManager
)


class TestExampleUIHooksFactory(unittest.TestCase):
    def setUp(self):
        self.plugin = ExamplePlugin()
        self.ui_hooks_factory = self.plugin.ui_hooks_factories[0]

    def test_initialization(self):
        self.assertEqual(self.ui_hooks_factory.plugin_id, self.plugin.id)

    def test_create_ui_hooks_manager(self):
        self.assertIsInstance(
            self.ui_hooks_factory.create_ui_hooks_manager(),
            ExampleUIHooksManager)
