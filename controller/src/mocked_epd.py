"""Module exports MockedEPD class"""

from typing import Any, Union

from PIL import Image


class MockedEPD:
    """Mocked EPD class

    This class is used to mock EPD object from waveshare library.
    It mocks an Epaper Display - instead of displaying the data
    on a physical display it outputs the data to a .png file.
    """

    def __init__(self, width: int, height: int) -> None:
        """MockedEPD constructor method"""
        self.width = width
        self.height = height

    def init(self, *args: Any, **kwargs: Any) -> None:
        """EPD.init mock"""

    # pylint: disable=C0103,W0613
    def Clear(self, color: Union[int, tuple[int], tuple[int, int, int], tuple[int, int, int, int], str, float, tuple[float]],
              *args: Any, **kwargs: Any) -> None:
        """EPD.Clear mock"""
        image = Image.new('1', (self.width, self.height), color)
        self.display(self.getbuffer(image))

    def getbuffer(self, image: Image.Image) -> Image.Image:
        """EPD.getbuffer mock"""
        return image

    def display(self, image: Image.Image, file_name: str = 'mocked_epd.png') -> None:
        """EPD.display mock"""
        image.save(file_name)
