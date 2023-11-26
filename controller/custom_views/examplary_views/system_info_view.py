"""
SystemInfo view class
"""

from typing import Any, Optional

from PIL import Image, ImageDraw, ImageFont
import psutil
from psutil._common import shwtemp

from custom_views.examplary_views.base_view import BaseView
from logger import logger
from src.helpers import view_fallback


# pylint: disable=R0801
class SystemInfoView(BaseView):
    """
    SystemInfo view is displaying: CPU temperature, disk usage, CPU utilization, memory usage and swapped memory usage.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.temperature: Optional[float] = None
        self.disk_usage: Optional[float] = None
        self.cpu_percent: Optional[float] = None
        self.virtual_memory: Optional[float] = None
        self.swap_memory: Optional[float] = None

    @view_fallback
    def _epd_change(self, first_call: bool) -> None:
        """
        IMPORTANT!

        Below positions of text and font sizes are chosen arbitrary and they are adjusted to 200x200 EPD, adjust them to your needs!
        """
        logger.info("%s is running", self.name)

        image = Image.new("1", (self.epd.width, self.epd.height), 255)

        draw = ImageDraw.Draw(image)
        font_small = ImageFont.truetype(
            "/usr/share/fonts/truetype/msttcorefonts/Impact.ttf", 36
        )
        font_awesome = ImageFont.truetype(
            "/usr/share/fonts/truetype/font-awesome/fontawesome-webfont.ttf", 36
        )

        draw.text((12, 6), "\uf2c9", font=font_awesome, fill=0)
        draw.text((50, 0), str(self.temperature) + " °C", font=font_small, fill=0)

        draw.text((6, 42), "\uf0a0", font=font_awesome, fill=0)
        draw.text((50, 36), str(self.disk_usage) + " %", font=font_small, fill=0)

        draw.text((7, 80), "\uf2db", font=font_awesome, fill=0)
        draw.text((50, 74), str(self.cpu_percent) + " %", font=font_small, fill=0)

        draw.text((4, 118), "\uf0f2", font=font_awesome, fill=0)
        draw.text((50, 112), str(self.virtual_memory) + " %", font=font_small, fill=0)

        draw.text((4, 158), "\uf0fa", font=font_awesome, fill=0)
        draw.text((50, 152), str(self.swap_memory) + " %", font=font_small, fill=0)

        self.image = image
        self._rotate_image()
        self.epd.display(self.epd.getbuffer(self.image))

    def _get_system_info(self) -> tuple[Optional[float], ...]:
        try:
            temperature = (
                psutil.sensors_temperatures()
                .get(
                    "cpu_thermal",
                    [shwtemp(label="cpu_thermal", current=0.0, high=0.0, critical=0.0)],
                )[0]
                .current
            )
            disk_usage = psutil.disk_usage("/").percent
            cpu_percent = psutil.cpu_percent()
            virtual_memory = psutil.virtual_memory().percent
            swap_memory = psutil.swap_memory().percent
            data = [temperature, disk_usage, cpu_percent, virtual_memory, swap_memory]
            return tuple(round(value, 1) for value in data)
        except Exception:  # pylint: disable=W0703
            logger.error("Unable to collect the data.")
            return (None, None, None, None, None)

    def _conditional(self, *args: Any, **kwargs: Any) -> bool:
        (
            temp_temperature,
            temp_disk_usage,
            temp_cpu_percent,
            temp_virtual_memory,
            temp_swap_memory,
        ) = self._get_system_info()
        if None in (
            temp_temperature,
            temp_disk_usage,
            temp_cpu_percent,
            temp_virtual_memory,
            temp_swap_memory,
        ):
            return False
        if bool(kwargs["first_call"]) or (
            (
                temp_temperature,
                temp_disk_usage,
                temp_cpu_percent,
                temp_virtual_memory,
                temp_swap_memory,
            )
            != (
                self.temperature,
                self.disk_usage,
                self.cpu_percent,
                self.virtual_memory,
                self.swap_memory,
            )
        ):
            self.temperature = temp_temperature
            self.disk_usage = temp_disk_usage
            self.cpu_percent = temp_cpu_percent
            self.virtual_memory = temp_virtual_memory
            self.swap_memory = temp_swap_memory
            return True
        return False
