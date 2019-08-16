import unittest

try:
    # It's possible to install the example plugins in a headless system or
    # in a environment without wfmanager and the graphical stack for UIs.
    #
    # This module depends on UIs so won't be tested in this case.
    from chaco.lineplot import LinePlot

    from force_wfmanager.model.analysis_model import AnalysisModel
    from force_wfmanager.ui.review.plot import ChacoPlot

    from enthought_example.example_data_views.example_data_view import (
        ExampleCustomPlot)
except ModuleNotFoundError:
    raise unittest.SkipTest(
        "No wfmanager found in the test environment. "
        "Data views can't be tested."
    )


class TestExampleCustomPlot(unittest.TestCase):

    def setUp(self):
        self.analysis_model = AnalysisModel()
        self.plot = ExampleCustomPlot(analysis_model=self.analysis_model)

    def test_init(self):
        self.assertIsInstance(self.plot._plot, ChacoPlot)
        self.assertIsInstance(self.plot._axis, LinePlot)
        self.assertEqual(self.plot._axis.marker, "circle")
        self.assertEqual(self.plot.title, "Line plot")
