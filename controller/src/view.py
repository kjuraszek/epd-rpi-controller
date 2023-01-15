"""Module exports View class"""

import logging
from PIL import Image

from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class View:
    """View is a basic object which interacts with EPD

    To display the data on EPD an instance of View must be created.
    Also a show method must be implemented to display desired informations
    on a EPD device. To support fallback view (in case of show method failure)
    additionally a fallback_show method must be implemented.
    """

    def __init__(self, name, interval, view_angle=Config.VIEW_ANGLE):
        """View constructor method"""
        self.epd = None
        self.name = name
        self.interval = interval
        self.image = None
        self.view_angle = view_angle

    def show(self, first_call):
        """Method displays desired informations on a EPD device"""
        raise NotImplementedError

    def _rotate_image(self):
        """Method rotates by configured angle and updates the image"""
        if self.image and isinstance(self.image, Image.Image):
            self.image = self.image.rotate(self.view_angle)

    def fallback_show(self, *args, **kwargs):
        """Method shows a fallback view if a show method fails"""
        raise NotImplementedError
