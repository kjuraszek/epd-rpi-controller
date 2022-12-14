'''
View class
'''
from PIL import Image

from config import VIEW_ANGLE

class View:
    '''
    view
    '''
    def __init__(self, name, interval, view_angle = VIEW_ANGLE):
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
