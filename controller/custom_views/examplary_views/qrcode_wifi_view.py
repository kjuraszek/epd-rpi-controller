"""
QRCodeWiFiView class
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
class QRCodeWiFiView(BaseView):
    """
    View displays QRCode to connect to WiFi network.

    It uses environment variables to prepare connection string.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        load_dotenv()
        wifi_ssid = os.getenv("WIFI_SSID")
        wifi_pass = os.getenv("WIFI_PASS")
        wifi_type = os.getenv("WIFI_TYPE")
        wifi_hidden = os.getenv("WIFI_HIDDEN")
        if None in (wifi_ssid, wifi_pass, wifi_type):
            self.connection_string = None
        elif wifi_hidden == "true":
            self.connection_string = (
                f"WIFI:S:{wifi_ssid};T:{wifi_type};P:{wifi_pass};H:{wifi_hidden};"
            )
        else:
            self.connection_string = f"WIFI:S:{wifi_ssid};T:{wifi_type};P:{wifi_pass};;"

    @view_fallback
    def _epd_change(self, first_call: bool) -> None:
        """
        IMPORTANT!

        Below calculations (qr_size) are adjusted to 200x200 EPD, adjust them to your needs!
        Also check QR codes documentation.
        """
        logger.info("%s is running", self.name)
        if not self.connection_string:
            logger.error("Connection string not created, serving fallback image!")
            raise ValueError
        qr_code = qrcode.QRCode(
            version=6,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border=4,
        )
        # (2 * border + version * 4 + 17) * box_size
        qr_size = (2 * 4 + 6 * 4 + 17) * 4
        margin = (self.epd.width - qr_size) // 2

        qr_code.add_data(self.connection_string)
        qr_code.make(fit=True)
        img = qr_code.make_image(fill_color="black", back_color="white")

        image = Image.new("1", (self.epd.width, self.epd.height), 255)
        image.paste(img, (margin, margin))

        self.image = image
        self._rotate_image()
        self.epd.display(self.epd.getbuffer(self.image))
        logger.info("EPD updated with %s", self.name)
