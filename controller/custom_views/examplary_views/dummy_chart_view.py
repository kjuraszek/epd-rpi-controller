"""
Dummy chart view class
"""

import io
import random
from typing import Any, Optional

from matplotlib import ticker, pyplot

from custom_views.examplary_views.chart_view import ChartView
from logger import logger


# pylint: disable=R0801
class DummyChartView(ChartView):
    """
    View shows dummy basic chart with random data.
    """

    PLOT_TYPES = ['plot', 'scatter', 'bar', 'stem', 'step', 'stackplot']

    def __init__(self, *, plot_type: str = 'plot', **kwargs: Any) -> None:
        self.plot_type = plot_type
        super().__init__(**kwargs)

    def _get_data(self) -> Optional[dict[str, int]]:
        """Method gathers the data eg. from external API, processes it and returns as a dict."""

        numbers = [random.randint(1, 20) for _ in range(4)]
        labels = ['A', 'B', 'C', 'D']
        return dict(zip(labels, numbers))

    def _draw_plot(self) -> io.BytesIO:
        """Method draws a plot basing on the data and returns it as a bytes."""

        if self.plot_type not in DummyChartView.PLOT_TYPES:
            logger.error('Unsupported plot type: %s', self.plot_type)
            raise ValueError
        y_values = list(self.data.keys())
        x_values = list(self.data.values())

        fig = pyplot.figure(figsize=self.figsize).gca()
        fig.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        if None not in (self.x_label, self.y_label):
            fig.set_ylabel(self.y_label)
            fig.set_xlabel(self.x_label)

        plot_func = getattr(pyplot, self.plot_type)
        if self.plot_type == 'stem':
            plot_func(y_values, x_values, linefmt='k-')
        else:
            plot_func(y_values, x_values, color='black')

        if self.plot_adjustment:
            pyplot.subplots_adjust(*self.plot_adjustment)

        if self.plot_title:
            pyplot.title(self.plot_title)
        buffer = io.BytesIO()
        pyplot.savefig(buffer, format='png')
        pyplot.close()
        return buffer

    def _conditional(self, *args: Any, **kwargs: Any) -> bool:
        data = self._get_data()
        if not data:
            return False
        if bool(kwargs['first_call']) or (
                data != self.data):
            self.data = data
            return True
        return False
