"""
Module contains validation functions
"""

from logger import logger

from config import Config
from src import View
from custom_views import VIEWS


def validate_config() -> None:
    """Function validates configuration from .cfg and .env files"""
    try:
        assert None not in [Config.KAFKA_VIEW_MANAGER_TOPIC, Config.PRODUCER_INTERVAL, Config.EPD_MODEL,
                            Config.CLEAR_EPD_ON_EXIT, Config.VITE_API_PORT],\
            'KAFKA_VIEW_MANAGER_TOPIC, PRODUCER_INTERVAL, EPD_MODEL, CLEAR_EPD_ON_EXIT must be set'
        assert isinstance(Config.KAFKA_VIEW_MANAGER_TOPIC, str),\
            'KAFKA_VIEW_MANAGER_TOPIC must be a string'
        assert isinstance(Config.PRODUCER_INTERVAL, int) and Config.PRODUCER_INTERVAL >= 0,\
            'PRODUCER_INTERVAL must be an integer greater than 0 or equal'
        assert isinstance(Config.PRODUCER_ASC_ORDER, bool),\
            'PRODUCER_ASC_ORDER must be a boolean'
        assert isinstance(Config.STARTING_VIEW, int) and Config.STARTING_VIEW >= 0 and Config.STARTING_VIEW < len(VIEWS),\
            'STARTING_VIEW must be an integer greater than 0 or equal and less than length of VIEWS'
        assert isinstance(Config.EPD_MODEL, str),\
            'EPD_MODEL must be a string'
        assert isinstance(Config.CLEAR_EPD_ON_EXIT, bool),\
            'EPD_MODEL must be a boolean'
        assert isinstance(Config.VIEW_ANGLE, int),\
            'EPD_MODEL must be an integer'
        assert isinstance(Config.USE_BUTTONS, bool),\
            'EPD_MODEL must be a boolean'
        assert isinstance(Config.VITE_API_PORT, int),\
            'VITE_API_PORT must be an integer'
        if Config.EPD_MODEL == 'mock':
            assert isinstance(Config.MOCKED_EPD_WIDTH, int) and Config.MOCKED_EPD_WIDTH > 0,\
                'MOCKED_EPD_WIDTH must be an integer greater than 0'
            assert isinstance(Config.MOCKED_EPD_HEIGHT, int) and Config.MOCKED_EPD_HEIGHT > 0,\
                'MOCKED_EPD_HEIGHT must be an integer greater than 0'
        if Config.USE_BUTTONS:
            assert isinstance(Config.LEFT_BUTTON_PIN, int) and Config.LEFT_BUTTON_PIN > 0,\
                'LEFT_BUTTON_PIN must be an integer greater than 0'
            assert isinstance(Config.RIGHT_BUTTON_PIN, int) and Config.RIGHT_BUTTON_PIN > 0,\
                'RIGHT_BUTTON_PIN must be an integer greater than 0'
            assert Config.LEFT_BUTTON_PIN != Config.RIGHT_BUTTON_PIN,\
                'LEFT_BUTTON_PIN and RIGHT_BUTTON_PIN cannot be equal'
    except AssertionError as exception:
        logger.error('Error with validating config file - %s', exception.args[0])
        raise ValidationConfigException from exception


def validate_views() -> None:
    """Function validates custom views"""
    try:
        assert len(VIEWS) > 0, 'VIEWS must contain at least one element'
        assert all(isinstance(view, View) for view in VIEWS),\
            'VIEWS must contain only View type elements'
    except AssertionError as exception:
        logger.error('Error with validating views - %s', exception.args[0])
        raise ValidationViewException from exception


class ValidationConfigException(Exception):
    """Error with validating config file."""


class ValidationViewException(Exception):
    """Error with validating views."""
