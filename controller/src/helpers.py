'''
Module contains helper functions
'''

import logging

from config import Config
from src import View
from custom_views import VIEWS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_config():
    try:
        assert not None in [Config.KAFKA_VIEW_MANAGER_TOPIC, Config.PRODUCER_INTERVAL, Config.EPD_MODEL, Config.CLEAR_EPD_ON_EXIT],\
            'KAFKA_VIEW_MANAGER_TOPIC, PRODUCER_INTERVAL, EPD_MODEL, CLEAR_EPD_ON_EXIT must be set'
        assert type(Config.KAFKA_VIEW_MANAGER_TOPIC) is str,\
            'KAFKA_VIEW_MANAGER_TOPIC must be a string'
        assert type(Config.PRODUCER_INTERVAL) is int and Config.PRODUCER_INTERVAL >= 0,\
            'PRODUCER_INTERVAL must be an integer greater than 0 or equal'
        assert type(Config.PRODUCER_ASC_ORDER) is bool,\
            'PRODUCER_ASC_ORDER must be a boolean'
        assert type(Config.STARTING_VIEW) is int and Config.STARTING_VIEW >= 0 and Config.STARTING_VIEW < len(VIEWS),\
            'STARTING_VIEW must be an integer greater than 0 or equal and less than length of VIEWS'    
        assert type(Config.EPD_MODEL) is str,\
            'EPD_MODEL must be a string'
        assert type(Config.CLEAR_EPD_ON_EXIT) is bool,\
            'EPD_MODEL must be a boolean'
        assert type(Config.VIEW_ANGLE) is int,\
            'EPD_MODEL must be an integer'
        assert type(Config.USE_BUTTONS) is bool,\
            'EPD_MODEL must be a boolean'
        if Config.EPD_MODEL == 'mock':
            assert type(Config.MOCKED_EPD_WIDTH) is int and Config.MOCKED_EPD_WIDTH > 0,\
                'MOCKED_EPD_WIDTH must be an integer greater than 0'
            assert type(Config.MOCKED_EPD_HEIGHT) is int and Config.MOCKED_EPD_HEIGHT > 0,\
                'MOCKED_EPD_HEIGHT must be an integer greater than 0'
        if Config.USE_BUTTONS:
            assert type(Config.LEFT_BUTTON_PIN) is int and Config.LEFT_BUTTON_PIN > 0,\
                'LEFT_BUTTON_PIN must be an integer greater than 0'
            assert type(Config.RIGHT_BUTTON_PIN) is int and Config.RIGHT_BUTTON_PIN > 0,\
                'RIGHT_BUTTON_PIN must be an integer greater than 0'
            assert Config.LEFT_BUTTON_PIN != Config.RIGHT_BUTTON_PIN,\
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


def signal_handler(thread, *args):
    logger.info('Received Signal: %s, stopping the controller.', args[0])
    thread.stop_event.set()


class ValidationConfigException(Exception):
    '''Error with validating config file.'''


class ValidationViewException(Exception):
    '''Error with validating views.'''
