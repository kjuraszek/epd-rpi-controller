"""Module exports View class"""

from datetime import datetime
from typing import Any, Optional

from PIL import Image

from config import Config
from src.helpers import view_conditional


# pylint: disable=W0613

class View:
    """View is a basic object which interacts with EPD

    To display the data on EPD an instance of View must be created.
    Also a _epd_change method must be implemented to display desired informations
    on a EPD device. To support fallback view (in case of _epd_change method failure)
    additionally a _fallback method must be implemented.
    """

    def __init__(self, name: str, interval: int, view_angle: int = Config.VIEW_ANGLE) -> None:
        """View constructor method"""
        self.epd: Any = None
        self.name = name
        self.interval = interval
        self.image: Optional[Image.Image] = None
        self.view_angle = view_angle
        self.timestamp: Optional[str] = None
        self.busy = False

    @view_conditional
    def show(self, first_call: bool) -> None:
        """Method is an entrypoint to display informations on EPD device.
        It sets certain properties of the current view and runs a method which operates
        directly on the EPD.
        """
        self._before_epd_change()
        self._epd_change(first_call)
        self._after_epd_change()

    def _before_epd_change(self) -> None:
        """Method sets view as busy before EPD change"""
        self.busy = True

    def _epd_change(self, first_call: bool) -> None:
        """Method displays desired informations on a EPD device"""
        raise NotImplementedError

    def _after_epd_change(self) -> None:
        """Method rotates the image, sets the timestamp and sets view as idle after EPD change"""
        self._set_timestamp()
        self.busy = False

    def _rotate_image(self) -> None:
        """Method rotates by configured angle and updates the image"""
        if self.image and isinstance(self.image, Image.Image):
            self.image = self.image.rotate(self.view_angle)

    def _set_timestamp(self) -> None:
        """Method sets a timestamp"""
        current_date = datetime.now()
        self.timestamp = current_date.strftime("%Y-%m-%d, %H:%M:%S")

    def _fallback(self, *args: Any, **kwargs: Any) -> None:
        """Method shows a fallback view if a _epd_change method fails"""
        raise NotImplementedError

    def _conditional(self, *args: Any, **kwargs: Any) -> bool:
        """Method used to trigger EPD change only under certain conditions"""
        return True
