"""
QRCodeUiView class
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
class QRCodeUiView(BaseView):
    """
    View displays QRCode with a link to use Controller's UI in the browser.

    It uses environment variables to prepare URL.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        load_dotenv()
        VITE_UI_PORT = os.getenv('VITE_UI_PORT')
        ADDRESS = os.getenv('VITE_HOSTNAME')
        PROTOCOL = 'http'
        if None in (VITE_UI_PORT, ADDRESS):
            self.url = None
        else:
            self.url = f'{PROTOCOL}://{ADDRESS}:{VITE_UI_PORT}'

    @view_fallback
    def _epd_change(self, first_call):
        logger.info('%s is running', self.name)
        '''
        IMPORTANT!
        
        Below calculations (qr_size) are adjusted to 200x200 EPD, adjust them to your needs!
        Also check QR codes documentation.
        '''
        if not self.url:
            logger.error('URL not created, serving fallback image!')
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

        qr.add_data(self.url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        image.paste(img, (margin, margin))

        self.image = image
        self.epd.display(self.epd.getbuffer(self.image))
        logger.info('EPD updated with %s', self.name)

