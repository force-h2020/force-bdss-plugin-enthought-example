import unittest

try:
    # It's possible to install the example plugins in a headless system or
    # in a environment without wfmanager and the graphical stack for UIs.
    #
    # This module depends on UIs so won't be tested in this case.
    from chaco.lineplot import LinePlot

    from force_wfmanager.model.analysis_model import AnalysisModel
    from force_wfmanager.ui.ui_utils import model_info

    from eggbox_potential_sampler.sampling_data_view.\
        sampling_data_view import SamplingDataView
except ModuleNotFoundError:
    raise unittest.SkipTest(
        "No wfmanager found in the test environment. "
        "Data views can't be tested."
    )


class TestSamplingDataView(unittest.TestCase):

    def setUp(self):
        self.analysis_model = AnalysisModel()
        self.data_view = SamplingDataView(analysis_model=self.analysis_model)

    def test_data_view(self):
        # check the view composition
        self.assertEqual(
            model_info(self.data_view), ['colormap_plot', 'sampling_plot']
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

    def check_update_is_requested_and_apply(self):
        # check
        self.assertTrue(self.plot.update_required)
        self.assertTrue(self.plot.plot_updater.active)
        # update
        self.plot.update_data_arrays()
        self.plot._update_plot()
        self.plot.update_required = False

    def add_data_points(self):
        # non monotonic convergence
        for datum in [
                (1, 3, 8), (2, 5, 7.7), (3, 2.6, 7.6), (4, 2.5, 7.62),
                (5, 2.47, 7.543), (6, 2.465, 7.54)]:
            self.analysis_model.add_evaluation_step(datum)
        self.check_update_is_requested_and_apply()

    def test_init(self):
        self.assertIsInstance(self.plot._axis, LinePlot)

    def test_resize_plot(self):
        ranges = self.plot.recenter_plot()
        self.assertEqual(ranges, (0.0, 1.0, -0.1, 1))
        self.add_data_points()
        self.plot._update_plot()

        ranges = self.plot._get_plot_range()
        # the second value for y (5) shouldn't contribute to the running min.
        self.assertEqual(ranges[3], 3.1)

    def test_change_variable(self):
        self.add_data_points()
        self.plot._update_plot()
        self.assertEqual(
            self.plot._custom_data_array, [3, 3, 2.6, 2.5, 2.47, 2.465])

        self.plot.y = "E"
        self.assertEqual(
            self.plot._custom_data_array, [8, 7.7, 7.6, 7.6, 7.543, 7.54])
