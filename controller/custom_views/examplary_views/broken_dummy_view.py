"""
Broken DummyView class
"""

import logging


from custom_views.examplary_views.dummy_view import DummyView
from src.helpers import view_fallback


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# pylint: disable=R0801
class BrokenDummyView(DummyView):
    """
    Broken DummyView class - it always serves a fallback image.
    """
    @view_fallback
    def _epd_change(self, first_call):
        raise NotImplementedError
