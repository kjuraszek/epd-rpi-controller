"""
Text view class
"""

import logging

from PIL import Image, ImageDraw, ImageFont

from custom_views.examplary_views.base_view import BaseView
from src.helpers import view_fallback, wrap_text


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# pylint: disable=R0801
class QuoteView(BaseView):
    """
    A simple view displaying static text adjusted to EPD size
    """

    def __init__(self, *, quote, author, **kwargs):
        super().__init__(**kwargs)
        self.quote = quote
        self.author = author

    @view_fallback
    def _epd_change(self, first_call):
        logger.info('%s is running', self.name)

        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)
        quote_font = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Trebuchet_MS_Bold_Italic.ttf', 16)
        author_font = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Impact.ttf', 18)

        wrapped_quote = wrap_text(self.epd.width, self.epd.height, quote_font, self.quote)
        wrapped_author = wrap_text(self.epd.width, self.epd.height, author_font, self.author)

        _, _, _, quote_height = draw.multiline_textbbox((0, 0), wrapped_quote, quote_font)

        draw.text((0, 10), str(wrapped_quote), font=quote_font, fill=0)
        draw.text((0, quote_height + 24), f'~ {wrapped_author}', font=author_font, fill=0)

        self.image = image
        self._rotate_image()
        self.epd.display(self.epd.getbuffer(self.image))
        logger.info('EPD updated with %s', self.name)
