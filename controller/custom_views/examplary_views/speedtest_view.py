"""
Speedtest view class
"""

import logging

from PIL import Image, ImageDraw, ImageFont
import speedtest

from custom_views.examplary_views.base_view import BaseView
from src.helpers import view_fallback


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# pylint: disable=R0801
class SpeedTestView(BaseView):
    """Speedtest view - it displays download and upload speed and ping"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.download = None
        self.upload = None
        self.ping = None

    @view_fallback
    def _epd_change(self, first_call):
        self._epd_in_progress()
        self._speed_test()
        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Impact.ttf', 26)
        font_awesome = ImageFont.truetype('/usr/share/fonts/truetype/font-awesome/fontawesome-webfont.ttf', 26)

        draw.text((5, 0), f'SpeedTest', font = font, fill = 0)
                
        draw.text((5, 50), u'\uf01a', font = font_awesome, fill = 0)
        draw.text((35, 46), f'{self.download} Mbps', font = font, fill = 0)
        
        draw.text((5, 90), u'\uf01b', font = font_awesome, fill = 0)
        draw.text((35, 86), f'{self.upload} Mbps', font = font, fill = 0)

        draw.text((4, 130), u'\uf1da', font = font_awesome, fill = 0)
        draw.text((35, 126), f'{self.ping}', font = font, fill = 0)
        
        self.image = image
        self.epd.display(self.epd.getbuffer(self.image))
        logger.info('EPD updated with %s', self.name)


    def _epd_in_progress(self):
        """Method updates epd with information about currently running test"""
        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Impact.ttf', 26)

        draw.text((5, 0), f'SpeedTest', font = font, fill = 0)
        draw.text((5, 30), f'. . . in progress', font = font, fill = 0)
        
        self.image = image
        self.epd.display(self.epd.getbuffer(self.image))
        logger.info('EPD updated with in progress %s', self.name)

    def _speed_test(self):     
        """Method runs speed test and sets ping, ul and dl speeds"""
        speedtest_client = speedtest.Speedtest()
        speedtest_client.get_servers()
        speedtest_client.get_best_server()
        speedtest_client.download()
        speedtest_client.upload()
        results = speedtest_client.results.dict()
        download = results.get('download', None)
        upload = results.get('upload', None)
        ping = results.get('ping', None)
        if None in (download, upload, ping):
            logger.error('Incomplete data, serving fallback image!')
            raise ValueError
        self.download = round(download/10**6, 2)
        self.upload = round(upload/10**6, 2)
        self.ping = int(ping)
