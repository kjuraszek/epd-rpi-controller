"""
Dummy view class
"""

import time
import logging

from PIL import Image, ImageDraw, ImageFont


from custom_views.examplary_views.base_view import BaseView
from src.helpers import view_fallback


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# pylint: disable=R0801
class DummyView(BaseView):
    """
    Dummy view displaying simple text.
    """

    @view_fallback
    def _epd_change(self, first_call):
        logger.info('%s is running', self.name)

        time.sleep(2)
        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Impact.ttf', self.epd.width//10)
        draw.text((self.epd.width//20, self.epd.height//20), f'Hello\nWorld from\n{self.name}', font=font, fill=0)
        self.image = image
        self._rotate_image()
        self.epd.display(self.epd.getbuffer(self.image))
        logger.info('EPD updated with %s', self.name)
