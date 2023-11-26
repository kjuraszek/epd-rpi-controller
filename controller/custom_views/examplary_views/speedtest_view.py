"""
Speedtest view class
"""

import time
from typing import Any, Optional

from PIL import Image, ImageDraw, ImageFont
import speedtest

from custom_views.examplary_views.base_view import BaseView
from logger import logger
from src.helpers import view_fallback


# pylint: disable=R0801
class SpeedTestView(BaseView):
    """Speedtest view - it displays download and upload speed and ping"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.download: Optional[Any] = None
        self.upload: Optional[Any] = None
        self.ping: Optional[int] = None

    @view_fallback
    def _epd_change(self, first_call: bool) -> None:
        self._epd_in_progress()
        self.busy = False
        time.sleep(2)
        self.busy = True
        self._speed_test()
        image = Image.new("1", (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/msttcorefonts/Impact.ttf", 26
        )
        font_awesome = ImageFont.truetype(
            "/usr/share/fonts/truetype/font-awesome/fontawesome-webfont.ttf", 26
        )

        draw.text((5, 0), "SpeedTest", font=font, fill=0)

        draw.text((5, 50), "\uf01a", font=font_awesome, fill=0)
        draw.text((35, 46), f"{self.download} Mbps", font=font, fill=0)

        draw.text((5, 90), "\uf01b", font=font_awesome, fill=0)
        draw.text((35, 86), f"{self.upload} Mbps", font=font, fill=0)

        draw.text((4, 130), "\uf1da", font=font_awesome, fill=0)
        draw.text((35, 126), f"{self.ping}", font=font, fill=0)

        self.image = image
        self._rotate_image()
        self.epd.display(self.epd.getbuffer(self.image))
        logger.info("EPD updated with %s", self.name)

    def _epd_in_progress(self) -> None:
        """Method updates epd with information about currently running test"""
        image = Image.new("1", (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/msttcorefonts/Impact.ttf", 26
        )

        draw.text((5, 0), "SpeedTest", font=font, fill=0)
        draw.text((5, 30), ". . . in progress", font=font, fill=0)

        self.image = image
        self._rotate_image()
        self.epd.display(self.epd.getbuffer(self.image))
        logger.info("EPD updated with in progress %s", self.name)

    def _speed_test(self) -> None:
        """Method runs speed test and sets ping, ul and dl speeds"""
        speedtest_client = speedtest.Speedtest()
        speedtest_client.get_servers()
        speedtest_client.get_best_server()
        speedtest_client.download()
        speedtest_client.upload()
        results = speedtest_client.results.dict()
        download = results.get("download", None)
        upload = results.get("upload", None)
        ping = results.get("ping", None)
        if None in (download, upload, ping):
            logger.error("Incomplete data, serving fallback image!")
            raise ValueError
        self.download = round(download / 10**6, 2)
        self.upload = round(upload / 10**6, 2)
        self.ping = int(ping)
