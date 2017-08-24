import unittest

from force_bdss.api import DataValue
from enthought_example.example_mco.example_mco_factory import ExampleMCOFactory
from enthought_example.example_mco.parameters import (
    RangedMCOParameterFactory,
    RangedMCOParameter)

try:
    import mock
except ImportError:
    from unittest import mock

from envisage.plugin import Plugin


class TestExampleMCOCommunicator(unittest.TestCase):
    def test_receive_from_mco(self):
        factory = ExampleMCOFactory(mock.Mock(spec=Plugin))
        mock_parameter_factory = mock.Mock(spec=RangedMCOParameterFactory)
        model = factory.create_model()
        model.parameters = [
            RangedMCOParameter(mock_parameter_factory)
        ]
        comm = factory.create_communicator()

        with mock.patch("sys.stdin") as stdin:
            stdin.read.return_value = "1"

            data = comm.receive_from_mco(model)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0].value, 1)
            self.assertEqual(data[0].type, "")

    def test_send_to_mco(self):
        factory = ExampleMCOFactory(mock.Mock(spec=Plugin))
        model = factory.create_model()
        comm = factory.create_communicator()

        with mock.patch("sys.stdout") as stdout:
            dv = DataValue(value=100)
            comm.send_to_mco(model, [dv, dv])
            self.assertEqual(stdout.write.call_args[0][0], '100 100')

            comm.send_to_mco(model, [])
            self.assertEqual(stdout.write.call_args[0][0], '')
