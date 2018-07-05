import unittest

try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.api import BaseMCOFactory

from enthought_example.example_mco.parameters import (
    RangedMCOParameter,
    RangedMCOParameterFactory
)

from enthought_example.example_mco.example_mco_model import ExampleMCOModel
from enthought_example.example_mco.example_mco import ExampleMCO


class TestExampleMCO(unittest.TestCase):
    def setUp(self):
        self.factory = mock.Mock(spec=BaseMCOFactory)
        self.factory.plugin = mock.Mock()
        self.factory.plugin.application = mock.Mock()
        self.factory.plugin.application.workflow_filepath = "whatever"

    def test_initialization(self):
        opt = ExampleMCO(self.factory)
        self.assertEqual(opt.factory, self.factory)

    def test_run(self):
        opt = ExampleMCO(self.factory)
        model = ExampleMCOModel(self.factory)
        model.parameters = [
            RangedMCOParameter(
                mock.Mock(spec=RangedMCOParameterFactory),
                lower_bound=1,
                upper_bound=3,
                initial_value=2)
        ]

        mock_process = mock.Mock()
        mock_process.communicate = mock.Mock(return_value=(b"1 2 3", b""))

        with mock.patch("subprocess.Popen") as mock_popen:
            mock_popen.return_value = mock_process
            opt.run(model)

        self.assertEqual(mock_popen.call_count, 2)