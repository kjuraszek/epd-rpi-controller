"""
Weather forecast daily view class
"""

import io
from typing import Any, Optional

from PIL import Image

from custom_views.examplary_views.base_view import BaseView
from logger import logger
from src.helpers import view_fallback


# pylint: disable=R0801
class ChartView(BaseView):
    """
    Chart view is a boilerplate for chart views.

    Methods _get_data and _draw_plot must be implemented in child class in order to work properly - see DummyChartView.
    """
    def __init__(self, *, figsize: tuple[float], plot_adjustment: Optional[tuple[float]] = None,
                 x_label: Optional[str], y_label: Optional[str], **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.figsize = figsize
        self.plot_adjustment = plot_adjustment
        self.x_label = x_label
        self.y_label = y_label
        self.data: dict[Any, Any] = {}

    @view_fallback
    def _epd_change(self, first_call: bool) -> None:
        logger.info('%s is running', self.name)

        plot = self._draw_plot()

        image = Image.open(plot)
        if image.size != (self.epd.width, self.epd.height):
            image = image.resize((self.epd.width, self.epd.height))
        image = image.convert('1')

        self.image = image
        self._rotate_image()
        self.epd.display(self.epd.getbuffer(self.image))

    def _get_data(self) -> Optional[dict[Any, Any]]:
        """Method gathers the data eg. from external API, processes it and returns as a dict."""
        raise NotImplementedError

    def _draw_plot(self) -> io.BytesIO:
        """Method draws a plot basing on the data and returns it as a bytes."""
        raise NotImplementedError

    def _conditional(self, *args: Any, **kwargs: Any) -> bool:
        data = self._get_data()
        if not data:
            return False
        if bool(kwargs['first_call']) or (
                data != self.data):
            self.data = data
            return True
        return False
