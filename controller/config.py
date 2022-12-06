import configparser

cfg = configparser.ConfigParser()
cfg.read('epd-rpi-controller.cfg')

PRODUCER_INTERVAL = cfg['main'].getint('producer_interval')
USE_MOCKED_EPD = cfg['main'].getboolean('use_mocked_epd')
MOCKED_EPD_WIDTH = cfg['main'].getint('mocked_epd_width')
MOCKED_EPD_HEIGHT = cfg['main'].getint('mocked_epd_height')
CLEAR_EPD_ON_EXIT = cfg['main'].getboolean('clear_epd_on_exit')
USE_BUTTONS = cfg['main'].getboolean('use_buttons')
LEFT_BUTTON_PIN = cfg['main'].getint('left_button_pin')
RIGHT_BUTTON_PIN = cfg['main'].getint('right_button_pin')
KAFKA_VIEW_MANAGER_TOPIC  = cfg['kafka'].get('view_manager_topic')
