'''
Examplary views
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
    def show(self):
        logger.info('%s is running', self.name)
        time.sleep(2)
                
        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Impact.ttf', 24)       
        draw.text((10, 10), f'Hello\nWorld from\n{self.name}', font = font, fill = 0)
        
        self.epd.display(self.epd.getbuffer(image))


VIEWS = [
    DummyView(None, 'Dummy view 1', 0),
    DummyView(None, 'Dummy view 2', 6),
    DummyView(None, 'Dummy view 3', 0),
    DummyView(None, 'Dummy view 4', 7)
]