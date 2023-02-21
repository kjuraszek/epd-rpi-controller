"""
QRCodeWiFiView class
"""

import logging
import os

from dotenv import load_dotenv
from PIL import Image
import qrcode

from custom_views.examplary_views.base_view import BaseView
from src.helpers import view_fallback


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# pylint: disable=R0801
class QRCodeWiFiView(BaseView):
    """
    View displays QRCode to connect to WiFi network.
    
    It uses environment variables to prepare connection string.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        load_dotenv()
        WIFI_SSID = os.getenv('WIFI_SSID')
        WIFI_PASS = os.getenv('WIFI_PASS')
        WIFI_TYPE = os.getenv('WIFI_TYPE')
        WIFI_HIDDEN = os.getenv('WIFI_HIDDEN')
        if None in (WIFI_SSID, WIFI_PASS, WIFI_TYPE):
            self.connection_string = None
        elif WIFI_HIDDEN == 'true':
            self.connection_string = f'WIFI:S:{WIFI_SSID};T:{WIFI_TYPE};P:{WIFI_PASS};H:{WIFI_HIDDEN};'
        else:
            self.connection_string = f'WIFI:S:{WIFI_SSID};T:{WIFI_TYPE};P:{WIFI_PASS};;'
        

    @view_fallback
    def _epd_change(self, first_call):
        logger.info('%s is running', self.name)
        '''
        IMPORTANT!
        
        Below calculations (qr_size) are adjusted to 200x200 EPD, adjust them to your needs!
        Also check QR codes documentation.
        '''
        if not self.connection_string:
            logger.error('Connection string not created, serving fallback image!')
            raise ValueError
        qr = qrcode.QRCode(
            version=6,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border=4,
        )
        # (2 * border + version * 4 + 17) * box_size
        qr_size = (2 * 4 + 6 * 4 + 17 ) * 4
        margin = (self.epd.width - qr_size)//2

        qr.add_data(self.connection_string)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        image.paste(img, (margin, margin))

        self.image = image
        self._rotate_image()
        self.epd.display(self.epd.getbuffer(self.image))
        logger.info('EPD updated with %s', self.name)

