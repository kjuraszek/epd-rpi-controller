'''
Module contains helper functions
'''

import logging

from config import KAFKA_VIEW_MANAGER_TOPIC, PRODUCER_INTERVAL, EPD_MODEL, MOCKED_EPD_WIDTH, MOCKED_EPD_HEIGHT, CLEAR_EPD_ON_EXIT, USE_BUTTONS, LEFT_BUTTON_PIN, RIGHT_BUTTON_PIN, VIEW_ANGLE
from src import View
from custom_views import VIEWS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_config():
    try:
        assert not None in [KAFKA_VIEW_MANAGER_TOPIC, PRODUCER_INTERVAL, EPD_MODEL, CLEAR_EPD_ON_EXIT],\
            'KAFKA_VIEW_MANAGER_TOPIC, PRODUCER_INTERVAL, EPD_MODEL, CLEAR_EPD_ON_EXIT must be set'
        assert type(KAFKA_VIEW_MANAGER_TOPIC) is str,\
            'KAFKA_VIEW_MANAGER_TOPIC must be a string'
        assert type(PRODUCER_INTERVAL) is int and PRODUCER_INTERVAL >= 0,\
            'PRODUCER_INTERVAL must be an integer greater than 0 or equal'
        assert type(EPD_MODEL) is str,\
            'EPD_MODEL must be a string'
        assert type(CLEAR_EPD_ON_EXIT) is bool,\
            'EPD_MODEL must be a boolean'
        assert type(VIEW_ANGLE) is int,\
            'EPD_MODEL must be an integer'
        assert type(USE_BUTTONS) is bool,\
            'EPD_MODEL must be a boolean'
        if EPD_MODEL == 'mock':
            assert type(MOCKED_EPD_WIDTH) is int and MOCKED_EPD_WIDTH > 0,\
                'MOCKED_EPD_WIDTH must be an integer greater than 0'
            assert type(MOCKED_EPD_HEIGHT) is int and MOCKED_EPD_HEIGHT > 0,\
                'MOCKED_EPD_HEIGHT must be an integer greater than 0'
        if USE_BUTTONS:
            assert type(LEFT_BUTTON_PIN) is int and LEFT_BUTTON_PIN > 0,\
                'LEFT_BUTTON_PIN must be an integer greater than 0'
            assert type(RIGHT_BUTTON_PIN) is int and RIGHT_BUTTON_PIN > 0,\
                'RIGHT_BUTTON_PIN must be an integer greater than 0'
            assert LEFT_BUTTON_PIN != RIGHT_BUTTON_PIN,\
                'LEFT_BUTTON_PIN and RIGHT_BUTTON_PIN cannot be equal'
    except AssertionError as e:
        logger.error(f'Error with validating config file - {e.args[0]}')
        raise ValidationConfigException from e


def validate_views():
    try:
        assert len(VIEWS) > 0, 'VIEWS must contain at least one element'
        assert all([isinstance(view, View) for view in VIEWS]),\
            'VIEWS must contain only View type elements'
    except AssertionError as e:
        logger.error(f'Error with validating views - {e.args[0]}')
        raise ValidationViewException from e


class ValidationConfigException(Exception):
    '''Error with validating config file.'''


class ValidationViewException(Exception):
    '''Error with validating views.'''
