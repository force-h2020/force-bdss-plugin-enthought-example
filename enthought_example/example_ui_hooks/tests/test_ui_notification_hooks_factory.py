import unittest

from envisage.api import Plugin

from enthought_example.example_ui_hooks.example_ui_hooks_factory import (
    ExampleUIHooksFactory)
from enthought_example.example_ui_hooks.example_ui_hooks_manager import (
    ExampleUIHooksManager
)

try:
    import mock
except ImportError:
    from unittest import mock


class TestExampleUIHooksFactory(unittest.TestCase):
    def test_initialization(self):
        mock_plugin = mock.Mock(spec=Plugin)
        factory = ExampleUIHooksFactory(mock_plugin)
        self.assertEqual(factory.plugin, mock_plugin)

    def test_create_ui_hooks_manager(self):
        mock_plugin = mock.Mock(spec=Plugin)
        factory = ExampleUIHooksFactory(mock_plugin)
        self.assertIsInstance(
            factory.create_ui_hooks_manager(),
            ExampleUIHooksManager)
