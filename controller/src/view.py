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

    def show(self):
        raise NotImplementedError

