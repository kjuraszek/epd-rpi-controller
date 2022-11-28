import configparser

cfg = configparser.ConfigParser()
cfg.read('epd-rpi-controller.cfg')

PRODUCER_INTERVAL = cfg['main'].getint('producer_interval')
USE_MOCKED_EPD = cfg['main'].getboolean('use_mocked_epd')
MOCKED_EPD_WIDTH = cfg['main'].getint('mocked_epd_width')
MOCKED_EPD_HEIGHT = cfg['main'].getint('mocked_epd_height')
KAFKA_VIEW_MANAGER_TOPIC  = cfg['kafka'].get('view_manager_topic')
