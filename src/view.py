'''
View class
'''

class View:
    '''
    view
    '''
    def __init__(self, epd, name, interval):
        self.epd = epd
        self.name = name
        self.interval = interval

    def show(self):
        raise NotImplementedError

