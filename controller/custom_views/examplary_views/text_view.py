"""
Text view class
"""

from typing import Any

from PIL import Image, ImageDraw, ImageFont

from custom_views.examplary_views.base_view import BaseView
from logger import logger
from src.helpers import view_fallback, wrap_text


# pylint: disable=R0801
class TextView(BaseView):
    """
    A simple view displaying static text adjusted to EPD size
    """

    def __init__(self, *, text: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.text = text

    @view_fallback
    def _epd_change(self, first_call: bool) -> None:
        logger.info("%s is running", self.name)

        image = Image.new("1", (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/msttcorefonts/Georgia_Italic.ttf", 20
        )

        wrapped_title = wrap_text(self.epd.width, self.epd.height, font, self.text)
        draw.text((0, 0), str(wrapped_title), font=font, fill=0)

        self.image = image
        self._rotate_image()
        self.epd.display(self.epd.getbuffer(self.image))
        logger.info("EPD updated with %s", self.name)
