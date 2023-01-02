import configparser
from dataclasses import dataclass
import os

cfg = configparser.ConfigParser()
cfg.read('epd-rpi-controller.cfg')

@dataclass
class Config:
    PRODUCER_INTERVAL = cfg['main'].getint('producer_interval')
    PRODUCER_ASC_ORDER = cfg['main'].getboolean('producer_asc_order')
    STARTING_VIEW = cfg['main'].getint('starting_view')
    EPD_MODEL = cfg['main'].get('epd_model')
    MOCKED_EPD_WIDTH = cfg['main'].getint('mocked_epd_width')
    MOCKED_EPD_HEIGHT = cfg['main'].getint('mocked_epd_height')
    CLEAR_EPD_ON_EXIT = cfg['main'].getboolean('clear_epd_on_exit')
    VIEW_ANGLE = cfg['main'].getint('view_angle')
    USE_BUTTONS = cfg['main'].getboolean('use_buttons')
    LEFT_BUTTON_PIN = cfg['main'].getint('left_button_pin')
    RIGHT_BUTTON_PIN = cfg['main'].getint('right_button_pin')
    KAFKA_VIEW_MANAGER_TOPIC  = cfg['kafka'].get('view_manager_topic')

    KAFKA_BOOTSTRAP_SERVER = 'kafka:29092' if 'EPD_RPI_DOCKERIZED' in os.environ else 'localhost:9092'
