import logging

import numpy as np

from traits.api import List, Instance, on_trait_change
from traitsui.api import View, VGroup, HGroup, Item, UItem, EnumEditor
from enable.api import ComponentEditor
from chaco.tools.api import PanTool, ZoomTool

from force_wfmanager.ui.review.base_data_view import BaseDataView
from force_wfmanager.ui.review.plot import Plot
from force_wfmanager.ui.review.plot import BasePlot, ChacoPlot

log = logging.getLogger(__name__)


class ConvergencePlot(BasePlot):
    """ This is an example of a more complicated plot that could be
    contributed by a plugin.

    Here, the running minimum of the y-values is displayed on a line
    plot.
    """

    #: Extra array to hold our custom plot data
    _custom_data_array = List()

    def _axis_hgroup_default(self):
        """Simple re-labelling of the underlying :class:`BasePlot` trait."""
        return HGroup(
            Item("y",
                 label="Convergence Variable",
                 editor=EnumEditor(name="displayable_value_names")),
        )

    def default_traits_view(self):
        """Implemented to removes the reset_plot option from the
        parent class View"""
        view = View(
            VGroup(
                self.axis_hgroup,
                UItem("_plot", editor=ComponentEditor()),
            )
        )
        return view

    def plot_cumulative_line(self):
        """ Create the Chaco line plot. """
        plot = ChacoPlot(self._plot_data)
        line_plot = plot.plot(
            ('x', 'y'),
            type='line',
            name='Line plot',
            marker='circle',
            bgcolor='white')[0]

        line_plot.tools.append(PanTool(plot))
        line_plot.overlays.append(ZoomTool(plot))

        self._plot_index_datasource = line_plot.index
        plot.trait_set(title=self.title, padding=75, line_width=1)
        self._axis = line_plot

        return plot

    def _update_plot_y_data(self):
        """ Update data points displayed by the y axis. Updates
        the convergence data in _custom_data_array
        Sets the y-`self._plot_data` to corresponding data in the
        `self._custom_data_array`.
        This method is called by the `_update_plot` method during
        the callback update.
        This method is called when the `y` axis is changed.
        """
        if self.y == "" or len(self.analysis_model.evaluation_steps) == 0:
            self._plot_data.set_data("y", [])
        else:
            self._plot.y_axis.title = self.y
            self._custom_data_array[:] = self._y_convergence_data()
            self._plot_data.set_data("y", self._custom_data_array)

    def _update_plot_x_data(self):
        """ Update data points displayed by the x axis.
        Sets the x-`self._plot_data` to corresponding data in the
        `self.data_arrays`.
        This method is called by the `_update_plot` method during
        the callback update.
        This method is called when the `x` axis is changed.
        """
        self._plot.x_axis.title = self.x
        x_array = np.arange(len(self._custom_data_array))
        self._plot_data.set_data("x", x_array)

    def __plot_default(self):
        """ Set the new default plot. """
        return self.plot_cumulative_line()

    def _y_convergence_data(self):
        """Calculates convergence data to display in the y axis"""
        new_data_array = []

        column = self.analysis_model.column(self.y)

        for ind, _ in enumerate(column, start=1):
            new_data_array.append(min(column[:ind]))

        return new_data_array

    @on_trait_change("displayable_value_names[]")
    def update_plot_axis_names(self):
        """This method overrides any changes in the super that occur
        to the x axis label"""
        super().update_plot_axis_names()

        self.x = "iteration"
        self._plot.x_axis.title = self.x

    def recenter_x_axis(self):
        """ Resets the bounds on the x-axis of the plot. If now x axis
        is specified, uses the default bounds (0, 1). Otherwise, infers
        the bounds from the x-axis related data."""
        if self._custom_data_array:
            max_x = 1.1 * len(self._custom_data_array)
            min_x = -0.1 * len(self._custom_data_array) + 1
            bounds = (min_x, max_x)
        else:
            bounds = (0, 1)

        self._set_plot_x_range(*bounds)
        self._reset_zoomtool()
        return bounds

    def recenter_y_axis(self):
        """ Resets the bounds on the x-axis of the plot. If now y axis
        is specified, uses the default bounds (-0.1, 1). Otherwise, infers
        the bounds from the y-axis related data."""
        if self._custom_data_array:
            max_y = max(self._custom_data_array) + 0.1
            min_y = min(self._custom_data_array) - 0.1
            bounds = (min_y, max_y)
        else:
            bounds = (-0.1, 1)

        self._set_plot_y_range(*bounds)
        self._reset_zoomtool()
        return bounds


class SamplingDataView(BaseDataView):
    """ This :class:`BaseDataView` shows two plot types side-by-side. """

    title = 'Potential Sampling'

    description = 'Potential sampling data view'

    colormap_plot = Instance(Plot)

    sampling_plot = Instance(ConvergencePlot)

    def default_traits_view(self):
        view = View(
            HGroup(
                UItem('colormap_plot', style='custom'),
                UItem('sampling_plot', style='custom')
            )
        )
        return view

    def _colormap_plot_default(self):
        cmap_plot = Plot(analysis_model=self.analysis_model,
                         title='Potential energy surface',
                         color_plot=True, is_active_view=self.is_active_view)
        self.sync_trait("is_active_view", cmap_plot)
        return cmap_plot

    def _sampling_plot_default(self):
        conv_plot = ConvergencePlot(analysis_model=self.analysis_model,
                                    title='Convergence',
                                    is_active_view=self.is_active_view)
        self.sync_trait("is_active_view", conv_plot)
        return conv_plot
