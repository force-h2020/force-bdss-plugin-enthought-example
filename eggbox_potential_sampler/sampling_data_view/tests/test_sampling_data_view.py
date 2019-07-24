import textwrap
import unittest

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

    def test_convergence_plot(self):
        # sampling_plot = self.data_view.sampling_plot
        pass
