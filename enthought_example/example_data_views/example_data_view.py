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
        plot.set(title=self.title)

        return plot

    def __plot_default(self):
        self._plot = self.plot_line()
        return self._plot
