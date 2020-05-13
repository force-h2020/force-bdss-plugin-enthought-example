#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import unittest

from enthought_example.example_plugin import ExamplePlugin
from force_bdss.api import DataValue

from unittest import mock


class TestExampleMCOCommunicator(unittest.TestCase):
    def setUp(self):
        self.plugin = ExamplePlugin()
        self.factory = self.plugin.mco_factories[0]

    def test_receive_from_mco(self):
        model = self.factory.create_model()
        parameter_factory = self.factory.parameter_factories[0]
        model.parameters = [
            parameter_factory.create_model()
        ]
        comm = self.factory.create_communicator()

        with mock.patch("sys.stdin") as stdin:
            stdin.read.return_value = "1"

            data = comm.receive_from_mco(model)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0].value, 1)
            self.assertEqual(data[0].type, "")

    def test_send_to_mco(self):
        model = self.factory.create_model()
        comm = self.factory.create_communicator()

        with mock.patch("sys.stdout") as stdout:
            dv = DataValue(value=100)
            comm.send_to_mco(model, [dv, dv])
            self.assertEqual(stdout.write.call_args[0][0], '100 100')

            comm.send_to_mco(model, [])
            self.assertEqual(stdout.write.call_args[0][0], '')
