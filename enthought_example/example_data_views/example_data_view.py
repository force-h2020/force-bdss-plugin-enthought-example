#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from force_wfmanager.ui import BasePlot


class ExampleCustomPlot(BasePlot):
    """ This is an example of a custom plot, that replaces
    the default scatter plot with a line plot.

    """

    title = 'Line plot'

    description = 'Example line plot'

    def plot_line(self, plot):
        line_plot = plot.plot(
            ('x', 'y'),
            type='line',
            name='Line plot',
            marker='circle',
            bgcolor='white')[0]

        self._axis = line_plot
        plot.trait_set(title=self.title)

    def customize_plot(self, plot):
        self.plot_line(plot)
