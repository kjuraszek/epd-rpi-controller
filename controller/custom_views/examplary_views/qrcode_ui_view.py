"""
QRCodeUiView class
"""

import os
from typing import Any

from dotenv import load_dotenv
from PIL import Image
import qrcode

from custom_views.examplary_views.base_view import BaseView
from logger import logger
from src.helpers import view_fallback


# pylint: disable=R0801
class QRCodeUiView(BaseView):
    """
    View displays QRCode with a link to use Controller's UI in the browser.

    It uses environment variables to prepare URL.
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        load_dotenv()
        vite_ui_port = os.getenv('VITE_UI_PORT')
        address = os.getenv('VITE_HOSTNAME')
        protocol = 'http'
        if None in (vite_ui_port, address):
            self.url = None
        else:
            self.url = f'{protocol}://{address}:{vite_ui_port}'

    @view_fallback
    def _epd_change(self, first_call: bool) -> None:
        '''
        IMPORTANT!

        Below calculations (qr_size) are adjusted to 200x200 EPD, adjust them to your needs!
        Also check QR codes documentation.
        '''

        logger.info('%s is running', self.name)

        if not self.url:
            logger.error('URL not created, serving fallback image!')
            raise ValueError
        qr_code = qrcode.QRCode(version=6,
                                error_correction=qrcode.constants.ERROR_CORRECT_L,
                                box_size=4, border=4)
        # (2 * border + version * 4 + 17) * box_size
        qr_size = (2 * 4 + 6 * 4 + 17) * 4
        margin = (self.epd.width - qr_size)//2

        qr_code.add_data(self.url)
        qr_code.make(fit=True)
        img = qr_code.make_image(fill_color="black", back_color="white")

        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        image.paste(img, (margin, margin))

        self.image = image
        self._rotate_image()
        self.epd.display(self.epd.getbuffer(self.image))
        logger.info('EPD updated with %s', self.name)
