'''
Module contains helper functions
'''

from config import KAFKA_VIEW_MANAGER_TOPIC, PRODUCER_INTERVAL
from src.view import View
from src.example import VIEWS


def validate_config():
    assert not None in [KAFKA_VIEW_MANAGER_TOPIC, PRODUCER_INTERVAL]
    assert type(KAFKA_VIEW_MANAGER_TOPIC) is str
    assert type(PRODUCER_INTERVAL) is int and PRODUCER_INTERVAL >= 0


def validate_views():
    assert all([isinstance(view, View) for view in VIEWS])
