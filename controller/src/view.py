'''
View class
'''
import logging
from PIL import Image

from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class View:
    '''
    view
    '''
    def __init__(self, name, interval, view_angle = Config.VIEW_ANGLE):
        self.epd = None
        self.name = name
        self.interval = interval
        self.image = None
        self.view_angle = view_angle

    def show(self, first_call):
        raise NotImplementedError

    def _rotate_image(self):
        if self.image and isinstance(self.image, Image.Image):
            self.image = self.image.rotate(self.view_angle)

    def fallback_show(self, *args, **kwargs):
        raise NotImplementedError

# class ViewFallback:
#     def __init__(self, view_class) -> None:
#         self.view_class = view_class

#     def __call__(self, func):
#         def wrapper(*args, **kwargs):
#             try:
#                 func(*args, **kwargs)
#             except KeyboardInterrupt:
#                 raise
#             except Exception as e:
#                 logger.exception(f'Error occured in {self.view_class.name}, calling fallback')
#                 self.view_class.fallback_show(*args, **kwargs)
#         return wrapper
