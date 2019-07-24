import unittest

from chaco.lineplot import LinePlot

from force_wfmanager.model.analysis_model import AnalysisModel
from force_wfmanager.ui.review.plot import ChacoPlot

from enthought_example.example_data_views.example_data_view import (
    ExampleCustomPlot)


class TestExampleCustomPlot(unittest.TestCase):

    def setUp(self):
        self.analysis_model = AnalysisModel()
        self.plot = ExampleCustomPlot(analysis_model=self.analysis_model)

    def test_init(self):
        self.assertIsInstance(self.plot._plot, ChacoPlot)
        self.assertIsInstance(self.plot._axis, LinePlot)
        self.assertEqual(self.plot._axis.marker, "circle")
        self.assertEqual(self.plot.title, "Line plot")
