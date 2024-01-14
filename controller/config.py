"""Configuration which is accessible throughout the application"""

import os
import configparser
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()
_CONFIG_FILE = os.getenv("EPD_RPI_CONFIG_FILE", "epd-rpi-controller.cfg")
cfg = configparser.ConfigParser()
cfg.read(_CONFIG_FILE)


@dataclass
class Config:
    """Config object which stores options from .cfg file and certain environment variables"""

    PRODUCER_INTERVAL = cfg["main"].getint("producer_interval")
    """Producer interval (in seconds).

    Based on ``producer_interval`` key in the ``main`` section from the config file.

    :meta hide-value:
    :type: int"""

    PRODUCER_ASC_ORDER = cfg["main"].getboolean("producer_asc_order")
    """Order of switching views, **yes** means ascending. Works only if `producer_interval` is set.

    Based on ``producer_asc_order`` key in the ``main`` section from the config file.

    :meta hide-value:
    :type: bool"""

    STARTING_VIEW = cfg["main"].getint("starting_view")
    """Index of View which will be the starting one.

    Based on ``starting_view`` key in the ``main`` section from the config file.

    :meta hide-value:
    :type: int"""

    EPD_MODEL = cfg["main"].get("epd_model")
    """EPD model which will be importen from Waveshare library.

    Based on ``epd_model`` key in the ``main`` section from the config file.

    :meta hide-value:
    :type: str"""

    MOCKED_EPD_WIDTH = cfg["main"].getint("mocked_epd_width")
    """Width of mocked EPD display (only used when `epd_model=mock`).

    Based on ``mocked_epd_width`` key in the ``main`` section from the config file.

    :meta hide-value:
    :type: int"""

    MOCKED_EPD_HEIGHT = cfg["main"].getint("mocked_epd_height")
    """Height of mocked EPD display (only used when `epd_model=mock`).

    Based on ``mocked_epd_height`` key in the ``main`` section from the config file.

    :meta hide-value:
    :type: int"""

    CLEAR_EPD_ON_EXIT = cfg["main"].getboolean("clear_epd_on_exit")
    """Clears display on exit when setted.

    Based on ``clear_epd_on_exit`` key in the ``main`` section from the config file.

    :meta hide-value:
    :type: bool"""

    VIEW_ANGLE = cfg["main"].getint("view_angle")
    """An angle by which the display will be rotated.

    Based on ``view_angle`` key in the ``main`` section from the config file.

    :meta hide-value:
    :type: int"""

    USE_BUTTONS = cfg["main"].getboolean("use_buttons")
    """Enables support for two physical buttons (left and right).

    Based on ``use_buttons`` key in the ``main`` section from the config file.

    :meta hide-value:
    :type: bool"""

    LEFT_BUTTON_PIN = cfg["main"].getint("left_button_pin")
    """GPIO number (not physical pin on board!) of pin connected to the left button.

    Based on ``left_button_pin`` key in the ``main`` section from the config file.

    :meta hide-value:
    :type: int"""

    RIGHT_BUTTON_PIN = cfg["main"].getint("right_button_pin")
    """GPIO number (not physical pin on board!) of pin connected to the right button.

    Based on ``right_button_pin`` key in the ``main`` section from the config file.

    :meta hide-value:
    :type: int"""

    CONFIG_FILE = _CONFIG_FILE
    """Name of the config file.

    Based on ``EPD_RPI_CONFIG_FILE`` environment variable.

    :meta hide-value:
    :type: str"""

    KAFKA_VIEW_MANAGER_TOPIC = cfg["kafka"].get("view_manager_topic")
    """Name of the topic used by Kafka.

    Based on ``view_manager_topic`` key in the ``kafka`` section from the config file.

    :meta hide-value:
    :type: str"""

    KAFKA_LOGGING_LEVEL = cfg["kafka"].get("logging_level")
    """Logging level for kafka.

    Based on ``logging_level`` key in the ``kafka`` section from the config file.

    :meta hide-value:
    :type: str"""

    MATPLOTLIB_LOGGING_LEVEL = cfg["matplotlib"].get("logging_level")
    """Logging level for matplotlib.

    Based on ``logging_level`` key in the ``matplotlib`` section from the config file.

    :meta hide-value:
    :type: str"""

    TORNADO_LOGGING_LEVEL = cfg["tornado"].get("logging_level")
    """Logging level for tornado.

    Based on ``logging_level`` key in the ``tornado`` section from the config file.

    :meta hide-value:
    :type: str"""

    KAFKA_BOOTSTRAP_SERVER = (
        "kafka:29092" if "EPD_RPI_DOCKERIZED" in os.environ else "localhost:9092"
    )
    """Kafka address

    is set to ``kafka:29092`` if environment variable ``EPD_RPI_DOCKERIZED`` is set, else: ``localhost:9092``.

    :meta hide-value:
    :type: str"""

    VITE_API_PORT = int(str(os.getenv("VITE_API_PORT")))
    """Port used by Controller's API and passed to UI.

    Based on ``VITE_API_PORT`` environment variable.

    :meta hide-value:
    :type: int"""
