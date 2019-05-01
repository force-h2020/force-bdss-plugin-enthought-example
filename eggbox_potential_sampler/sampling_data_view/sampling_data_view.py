from traits.api import on_trait_change, List, Instance, Enum
from traitsui.api import View, VGroup, HGroup, Item, UItem
from enable.api import ComponentEditor
from chaco.tools.api import PanTool, ZoomTool

from force_wfmanager.central_pane.data_view_pane import DataViewPane
from force_wfmanager.central_pane.plot import Plot
from force_wfmanager.central_pane.plot import BasePlot, ChacoPlot


class ConvergencePlot(BasePlot):
    """ This is an example of a more complicated plot that could be
    contributed by a plugin.

    Here, the running minimum of the y-values is displayed on a line
    plot.

    """

    #: Simple re-labelling of the underlying :class:`BasePlot` trait.
    y = Enum(values='_value_names', label='convergence variable')

    #: Extra array to hold our custom plot data
    _custom_data_array = List()

    #: The View of the plot, showing the menu to choose 'y' and the plot itself
    view = View(
        VGroup(
            HGroup(
                Item('y'),
            ),
            UItem('_plot', editor=ComponentEditor())
        )
    )

    def plot_cumulative_line(self):
        """ Create the Chaco line plot. """
        plot = ChacoPlot(self._plot_data)
        line_plot = plot.plot(
            ('iteration', 'cumulative_minimum'),
            type='line',
            name='Line plot',
            marker='circle',
            bgcolor='white')[0]

        line_plot.tools.append(PanTool(plot))
        line_plot.overlays.append(ZoomTool(plot))

        self._plot_index_datasource = line_plot.index
        plot.set(title=self.title, padding=75, line_width=1)
        self._axis = line_plot

        return plot

    @on_trait_change('x,y')
    def _update_plot_data(self):
        """ Override update_plot_data to include the new ancillary
        array, and an array containing the index of that array.

        """
        super()._update_plot_data()
        self._custom_data_array = []

        if self.y is None:
            return

        y_index = self.analysis_model.value_names.index(self.y)
        for ind, _ in enumerate(self._data_arrays[y_index], start=1):
            self._custom_data_array.append(
                min(self._data_arrays[y_index][:ind]))
        self._plot_data.set_data('cumulative_minimum',
                                 self._custom_data_array)
        self._plot_data.set_data(
            'iteration',
            list(range(1, len(self._custom_data_array) + 1))
        )

        self.resize_plot()

    def __plot_default(self):
        """ Set the new default plot. """
        self._plot = self.plot_cumulative_line()
        return self._plot

    def __plot_data_default(self):
        """ Add custom columns to the default plot data. """
        plot_data = self._get_plot_data_default()
        plot_data.set_data('cumulative_minimum', [])
        plot_data.set_data('iteration', [])
        return plot_data

    def resize_plot(self):
        """ Override resize plot based on the data we're actually
        plotting.

        """
        try:
            min_y = min(self._custom_data_array) - 0.1
        except ValueError:
            min_y = -0.1
        try:
            max_y = max(self._custom_data_array) + 0.1
        except ValueError:
            max_y = 1

        try:
            max_x = 1.1 * len(self._custom_data_array)
        except ValueError:
            max_x = 1
        try:
            min_x = -0.1 * len(self._custom_data_array) + 1
        except ValueError:
            min_x = 0

        ranges = (min_x, max_x, min_y, max_y)
        self._set_plot_range(*ranges)

        for idx, overlay in enumerate(self._plot.overlays):
            if isinstance(overlay, ZoomTool):
                self._plot.overlays[idx] = ZoomTool(self._plot)

        return ranges


class SamplingDataViewPane(DataViewPane):
    """ This :class:`DataViewPane` shows two plot types side-by-side. """

    name = 'Potential Sampling Data View'

    colormap_plot = Instance(Plot)
    sampling_plot = Instance(ConvergencePlot)

    traits_view = View(
        HGroup(UItem('colormap_plot', style='custom'),
               UItem('sampling_plot', style='custom')))

    def _colormap_plot_default(self):
        return Plot(analysis_model=self.analysis_model,
                    title='Potential energy surface',
                    color_plot=True)

    def _sampling_plot_default(self):
        return ConvergencePlot(analysis_model=self.analysis_model,
                               title='Convergence')
