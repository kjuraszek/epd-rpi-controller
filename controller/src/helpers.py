'''
Module contains helper functions
'''

from config import KAFKA_VIEW_MANAGER_TOPIC, PRODUCER_INTERVAL, USE_MOCKED_EPD, MOCKED_EPD_WIDTH, MOCKED_EPD_HEIGHT
from src import View
from custom_views import VIEWS


def validate_config():
    assert not None in [KAFKA_VIEW_MANAGER_TOPIC, PRODUCER_INTERVAL, USE_MOCKED_EPD]
    assert type(KAFKA_VIEW_MANAGER_TOPIC) is str
    assert type(PRODUCER_INTERVAL) is int and PRODUCER_INTERVAL >= 0
    assert type(USE_MOCKED_EPD) is bool
    if USE_MOCKED_EPD:
        assert type(MOCKED_EPD_WIDTH) is int and MOCKED_EPD_WIDTH > 0
        assert type(MOCKED_EPD_HEIGHT) is int and MOCKED_EPD_HEIGHT > 0


def validate_views():
    assert len(VIEWS) > 0
    assert all([isinstance(view, View) for view in VIEWS])
