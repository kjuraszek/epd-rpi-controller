'''
Examplary class DummyView and views
'''

import time
import logging

from PIL import Image, ImageDraw, ImageFont

from src import View

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DummyView(View):
    '''
    dummy view
    '''
    def show(self, first_call):
        logger.info('%s is running', self.name)
        time.sleep(2)

        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Impact.ttf', self.epd.width // 10)
        draw.text((self.epd.width // 20, self.epd.height // 20), f'Hello\nWorld from\n{self.name}', font = font, fill = 0)
        self.image = image
        self._rotate_image()
        self.epd.display(self.epd.getbuffer(self.image))


VIEWS = [
    DummyView('Dummy view 1', 0),
    DummyView('Dummy view 2', 6, 180),
    DummyView('Dummy view 3', 0),
    DummyView('Dummy view 4', 7)
]
