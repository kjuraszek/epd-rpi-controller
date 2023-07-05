"""
Clock view class
"""

import datetime
from logger import logger
from typing import Any, Optional

from PIL import Image, ImageDraw, ImageFont


from custom_views.examplary_views.base_view import BaseView
from src.helpers import view_fallback


# pylint: disable=R0801
class ClockView(BaseView):
    """Clock view - it displays current time and date"""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.current_time_date: tuple[Optional[str], Optional[str]] = (None, None)

    @view_fallback
    def _epd_change(self, first_call: bool) -> None:

        current_time, current_date = self.current_time_date
        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)
        big_font = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Impact.ttf', self.epd.width//3)
        font = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Impact.ttf', self.epd.width//6)
        draw.text((self.epd.width//20, self.epd.height//50), f'{current_time}', font=big_font, fill=0)
        draw.text((self.epd.width//20, self.epd.width//4 + self.epd.height//20),
                  f'----------------\n{current_date}', font=font, fill=0)
        self.image = image
        self._rotate_image()
        self.epd.display(self.epd.getbuffer(self.image))
        logger.info('EPD updated with %s', self.name)

    def _conditional(self, *args: Any, **kwargs: Any) -> bool:
        if self.busy:
            return False
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        current_date = now.strftime("%d/%m/%Y")
        if kwargs['first_call'] or self.current_time_date != (current_time, current_date):
            self.current_time_date = (current_time, current_date)
            return True
        return False
