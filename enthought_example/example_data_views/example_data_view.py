from pyface.timer.api import do_later

from force_wfmanager.ui.review.plot import BasePlot, ChacoPlot


class ExampleCustomPlot(BasePlot):
    """ This is an example of a custom plot, that replaces
    the default scatter plot with a line plot.

    """

    title = 'Line plot'

    description = 'Example line plot'

    def plot_line(self):
        plot = ChacoPlot(self._plot_data)
        line_plot = plot.plot(
            ('x', 'y'),
            type='line',
            name='Line plot',
            marker='circle',
            bgcolor='white')[0]

        self._plot_index_datasource = line_plot.index
        self._axis = line_plot
        plot.trait_set(title=self.title)

        return plot

    def __plot_default(self):
        plot = self.plot_line()
        self.plot_updater.start()
        do_later(self.recenter_plot)
        return plot
