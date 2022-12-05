'''
View class
'''

class View:
    '''
    view
    '''
    def __init__(self, name, interval):
        self.epd = None
        self.name = name
        self.interval = interval
        self.image = None

    def show(self):
        raise NotImplementedError

    def screenshot(self):
        return self.image
