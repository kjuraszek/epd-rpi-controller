'''
View class
'''
import logging
import functools
from PIL import Image

from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class View:
    '''
    view
    '''
    def fallback(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                func(self, *args, **kwargs)
            except KeyboardInterrupt:
                raise
            except Exception as e:
                logger.exception(f'Error occured in {self.name}, calling fallback')
                self._fallback_show(self, *args, **kwargs)
        return wrapper

    def __init__(self, name, interval, view_angle = Config.VIEW_ANGLE):
        self.epd = None
        self.name = name
        self.interval = interval
        self.image = None
        self.view_angle = view_angle

    def show(self, first_call):
        raise NotImplementedError

    def screenshot(self):
        return self.image

    def _rotate_image(self):
        if self.image and isinstance(self.image, Image.Image):
            self.image = self.image.rotate(self.view_angle)

    def _fallback_show(self, *args, **kwargs):
        raise NotImplementedError
