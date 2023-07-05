"""
Broken DummyView class
"""

from logger import logger


from custom_views.examplary_views.dummy_view import DummyView
from src.helpers import view_fallback


# pylint: disable=R0801
class BrokenDummyView(DummyView):
    """
    Broken DummyView class - it always serves a fallback image.
    """
    @view_fallback
    def _epd_change(self, first_call: bool) -> None:
        raise NotImplementedError
