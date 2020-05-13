#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import unittest

from unittest import mock

from enthought_example.tests.utils import captured_output
from enthought_example.example_ui_hooks.example_ui_hooks_factory import (
    ExampleUIHooksFactory
)
from enthought_example.example_ui_hooks.example_ui_hooks_manager import (
    ExampleUIHooksManager
)


class TestExampleUIHooksManager(unittest.TestCase):
    def test_initialization(self):
        mock_factory = mock.Mock(spec=ExampleUIHooksFactory)
        manager = ExampleUIHooksManager(factory=mock_factory)
        self.assertEqual(manager.factory, mock_factory)

    def test_before_and_after_execution(self):
        mock_factory = mock.Mock(spec=ExampleUIHooksFactory)
        manager = ExampleUIHooksManager(factory=mock_factory)

        mock_task = mock.Mock()
        with captured_output() as (stdout, stderr):
            manager.before_execution(mock_task)
            manager.after_execution(mock_task)
            manager.before_save(mock_task)

        self.assertEqual(
            stdout.getvalue(),
            ("This is the example UI hook. The execution is about to begin.\n"
             "This is the example UI hook. The execution is done.\n"
             "This is the example UI hook. The save is about to begin.\n"))
