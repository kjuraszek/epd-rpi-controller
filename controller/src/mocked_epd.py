"""Module exports MockedEPD class"""

from PIL import Image


class MockedEPD:
    """Mocked EPD class

    This class is used to mock EPD object from waveshare library.
    It mocks an Epaper Display - instead of displaying the data
    on a physical display it outputs the data to a .png file.
    """

    def __init__(self, width, height):
        """MockedEPD constructor method"""
        self.width = width
        self.height = height

    def init(self, *args, **kwargs):
        """EPD.init mock"""

    def Clear(self, color, *args, **kwargs):  # pylint: disable=C0103,W0613
        """EPD.Clear mock"""
        image = Image.new('1', (self.width, self.height), color)
        self.display(self.getbuffer(image))

    def getbuffer(self, image):
        """EPD.getbuffer mock"""
        return image

    def display(self, image, file_name='mocked_epd.png'):
        """EPD.display mock"""
        image.save(file_name)
