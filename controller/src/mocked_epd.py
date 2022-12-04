'''
Mocked EPD class
'''

from PIL import Image, ImageDraw, ImageFont

class MockedEPD:
    '''
    mocked epd
    '''
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def init(self, *args, **kwargs):
        pass

    def Clear(self, color, *args, **kwargs):
        image = Image.new('1', (self.width, self.height), color)
        self.display(self.getbuffer(image))

    def getbuffer(self, image):
        return image
    
    def display(self, image, file_name = 'mocked_epd.png'):
        image.save(file_name)