import textwrap
import unittest

from chaco.lineplot import LinePlot

from force_wfmanager.model.analysis_model import AnalysisModel

from eggbox_potential_sampler.sampling_data_view import (
    SamplingDataView)


class TestSamplingDataView(unittest.TestCase):

    def setUp(self):
        self.analysis_model = AnalysisModel()
        self.data_view = SamplingDataView(analysis_model=self.analysis_model)

    def test_data_view(self):
        # check the view composition (there are probably better ways of
        # checking a traitsui.view.View)
        expected_view = textwrap.dedent("""\
            ( HGroup(
                Item( 'colormap_plot'
                      object = 'object',
                      style  = 'custom'
                ),
                Item( 'sampling_plot'
                      object = 'object',
                      style  = 'custom'
                ),
                object = 'object',
                style  = 'simple'
            ) )""")
        self.assertEqual(
            repr(self.data_view.trait_view_elements().content["traits_view"]),
            expected_view
        )

        self.assertEqual(
            self.data_view.colormap_plot.title, 'Potential energy surface'
        )
        self.assertEqual(
            self.data_view.sampling_plot.title, 'Convergence'
        )


class TestConvergencePlot(unittest.TestCase):

    def setUp(self):
        self.analysis_model = AnalysisModel()
        self.data_view = SamplingDataView(analysis_model=self.analysis_model)
        self.plot = self.data_view.sampling_plot
        self.analysis_model.value_names = ("x", "y", "E")

    def add_data_points(self):
        # non monotonic convergence
        for datum in [
                (1, 3, 8), (2, 5, 7.7), (3, 2.6, 7.6), (4, 2.5, 7.62),
                (5, 2.47, 7.543), (6, 2.465, 7.54)]:
            self.analysis_model.add_evaluation_step(datum)

    def test_init(self):
        self.assertIsInstance(self.plot._axis, LinePlot)

    def test_resize_plot(self):
        ranges = self.plot.resize_plot()
        self.assertEqual(ranges, (1.0, 0.0, -0.1, 1))
        self.add_data_points()
        self.plot._update_plot_data()

        # running explicitely to catch the return
        ranges = self.plot.resize_plot()
        # the second value for y (5) shouldn't contribute to the running min.
        self.assertEqual(ranges[3], 3.1)

    def test_change_variable(self):
        self.add_data_points()
        self.plot._update_plot_data()
        self.assertEqual(
            self.plot._custom_data_array, [3, 3, 2.6, 2.5, 2.47, 2.465])

        self.plot.y = "E"
        self.assertEqual(
            self.plot._custom_data_array, [8, 7.7, 7.6, 7.6, 7.543, 7.54])
