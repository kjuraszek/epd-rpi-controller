'''
Mocked EPD class
'''

class MockedEPD:
    '''
    mocked epd
    '''
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def init(self, *args, **kwargs):
        pass

    def Clear(self, *args, **kwargs):
        pass

    def getbuffer(self, image):
        return image
    
    def display(self, image, file_name = 'mocked_epd.png'):
        image.save(file_name)