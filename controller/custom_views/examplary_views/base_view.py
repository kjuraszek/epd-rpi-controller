"""
Base View class
"""

import logging

from PIL import Image, ImageDraw, ImageFont

from src import View


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# pylint: disable=R0801


class BaseView(View):
    """
    Base View class - a base for View classes
    
    It has only defined _fallback method so _epd_change still must be defined in child classes.
    """

    def _fallback(self, *args, **kwargs):
        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Impact.ttf', self.epd.width//10)
        draw.text((self.epd.width//20, self.epd.height//20),
                  f'Unable to show:\n{self.name}\n\nDisplaying fallback', font=font, fill=0)
        self.image = image
        self._rotate_image()
        self.epd.display(self.epd.getbuffer(self.image))
        logger.info('EPD updated with fallback for %s', self.name)
