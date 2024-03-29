"""
Examplary usage of classes: DummyView, BrokenDummyView, ConditionalDummyView and VIEWS list
"""

# pylint: disable=R0801
from custom_views.examplary_views import (
    DummyView,
    BrokenDummyView,
    ConditionalDummyView,
    ClockView,
)


VIEWS = [
    DummyView(name="Dummy view 1", interval=0),
    DummyView(name="Dummy view 2", interval=6, view_angle=180),
    BrokenDummyView(name="Dummy view 3", interval=0),
    ConditionalDummyView(name="Dummy view 4", interval=4),
    ClockView(name="Clock", interval=1),
]
