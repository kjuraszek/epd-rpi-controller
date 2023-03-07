"""
Conditional DummyView class
"""

import logging
from typing import Any

from custom_views.examplary_views.dummy_view import DummyView


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# pylint: disable=R0801
class ConditionalDummyView(DummyView):
    """
    Conditional DummyView class - it updates EPD only when certain condition is met.
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.switch = False

    def _conditional(self, *args: Any, **kwargs: Any) -> bool:
        self.switch = not self.switch
        if bool(kwargs['first_call']) or self.switch:
            return True
        return False
