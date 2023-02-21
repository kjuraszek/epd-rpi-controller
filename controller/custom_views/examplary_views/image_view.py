"""
Image view class
"""

import time
import logging

from PIL import Image, ImageDraw, ImageFont


from custom_views.examplary_views.base_view import BaseView
from src.helpers import view_fallback


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# pylint: disable=R0801
class ImageView(BaseView):
    """
    Image view displaying the image from a file.
    """

    def __init__(self, *, image_path, **kwargs):
        super().__init__(**kwargs)
        self.image_path = image_path

    @view_fallback
    def _epd_change(self, first_call):
        logger.info('%s is running', self.name)

        image = Image.open(self.image_path)
        image_width, image_height = image.size
        if self.epd.width != image_width or self.epd.height != image_height:
            logger.error('Image and EPD dimensions are different!')
            raise ValueError
        self.image = image
        self._rotate_image()
        self.epd.display(self.epd.getbuffer(self.image))
        logger.info('EPD updated with %s', self.name)

