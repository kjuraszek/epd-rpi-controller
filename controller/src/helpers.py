"""
Module contains helper functions
"""

import functools
import logging

from PIL import Image, ImageDraw

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

def wrap_titles(epd_width, epd_height, font, titles):
    """Function wraps each title using newlines to fit in the EPD size based on used font"""

    wrapped_titles = []
    for title in titles:
        wrapped_title = wrap_text(epd_width, epd_height, font, title)
        image = Image.new('1', (200, 200), 255)
        draw = ImageDraw.Draw(image)
        _, _, text_width, text_height = draw.multiline_textbbox((0,0), wrapped_title, font)
        wrapped_titles.append({
            'wrapped_title': wrapped_title,
            'text_width': text_width,
            'text_height': text_height
            }
        )
    
    return wrapped_titles

def wrap_text(epd_width, epd_height, font, text):
    """Function wraps string using newlines to fit in the EPD size based on used font"""
    _, _,font_width, font_height = font.getbbox('.')
    if font_height > epd_height or font_width > epd_width:
        logger.error('Selected font is much larger than EPD dimensions!')
        raise ValueError
    lines = []
    start = 0
    for index, _ in enumerate(text):
        if index > 0:
            size = font.getlength(text[start:index])
            if size > epd_width:
                lines.append(text[start:index - 1] + '\n')
                start = index - 1
        if index == len(text) - 1:
            lines.append(text[start:])

    wrapped_text = ''.join(lines)
    return wrapped_text
