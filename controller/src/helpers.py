'''
Module contains helper functions
'''

import functools
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def signal_handler(thread, *args):
    logger.info('\nReceived Signal: %s, stopping the controller.', args[0])
    thread.stop_event.set()


# pylint: disable=E1102,W0703
def view_fallback(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        view_object = args[0]
        try:
            func(*args, **kwargs)
        except Exception:
            logger.exception('Error occured in %s, calling fallback', view_object.name)
            view_object.fallback_show(*args, **kwargs)
    return wrapper
