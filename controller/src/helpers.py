"""
Module contains helper functions
"""

import functools
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def signal_handler(thread, *args):
    """Signal handler

    Function is handling certain signal in such a way that it sets stop event for certain
    Thread-based class (it should be Consumer or ViewManager)
    """

    logger.info('\nReceived Signal: %s, stopping the controller.', args[0])
    thread.stop_event.set()


# pylint: disable=E1102,W0703
def view_fallback(func):
    """Function triggers _fallback method of View object if a _epd_change method fails"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        view_object = args[0]
        try:
            func(*args, **kwargs)
        except Exception:
            logger.exception('Error occured in %s, calling fallback', view_object.name)
            view_object._fallback(*args, **kwargs)
    return wrapper


# pylint: disable=E1102,W0703
def view_conditional(func):
    """Function triggers _epd_change method of View object only when _conditional method returns True"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        view_object = args[0]
        if view_object._conditional(*args, **kwargs):
            func(*args, **kwargs)
    return wrapper
