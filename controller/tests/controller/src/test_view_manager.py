"""
ViewManager class tests
"""

import sys
import pytest
import importlib
import time
from unittest.mock import Mock

import src.view_manager
from src.view_manager import ViewManager


class TestViewManager:
    def test_stop(self, mocker):
        mocked_epd = Mock()
        views = []
        view_manager = ViewManager(views, mocked_epd)
        view_manager.stop_event = Mock()
        view_manager.stop_event.set = Mock()

        view_manager.stop()
        view_manager.stop_event.set.assert_called_once()

    def test_next(self, mocker):
        mocked_epd = Mock()
        views = []
        view_manager = ViewManager(views, mocked_epd)

        view_manager.busy = Mock()
        view_manager.busy.is_set = Mock(return_value=True)
        view_manager.busy.set = Mock()

        view_manager.next()

        assert view_manager.action == None
        assert not view_manager.busy.set.called

        view_manager.busy.is_set = Mock(return_value=False)

        view_manager.next()

        assert view_manager.action == "next"
        assert view_manager.busy.set.called

    def test_prev(self, mocker):
        mocked_epd = Mock()
        views = []
        view_manager = ViewManager(views, mocked_epd)

        view_manager.busy = Mock()
        view_manager.busy.is_set = Mock(return_value=True)
        view_manager.busy.set = Mock()

        view_manager.prev()

        assert view_manager.action == None
        assert not view_manager.busy.set.called

        view_manager.busy.is_set = Mock(return_value=False)

        view_manager.prev()

        assert view_manager.action == "prev"
        assert view_manager.busy.set.called

    def test_run(self, mocker):
        mocked_epd = Mock()
        mocked_epd.init = Mock()
        mocked_epd.Clear = Mock()
        mocked_view_1 = Mock()
        mocked_view_1.interval = 0
        mocked_view_1.show = Mock()
        mocked_view_2 = Mock()
        mocked_view_2.interval = 0
        mocked_view_2.show = Mock()

        views = [mocked_view_1, mocked_view_2]
        view_manager = ViewManager(views, mocked_epd)

        view_manager.start()
        time.sleep(0.1)
        view_manager.stop()
        view_manager.join()

        assert mocked_epd.init.called
        assert mocked_epd.Clear.called
        assert mocked_view_1.show.called
        assert not mocked_view_2.show.called

    def test_run_with_next_action(self, mocker):
        mocked_epd = Mock()
        mocked_epd.init = Mock()
        mocked_epd.Clear = Mock()
        mocked_view_1 = Mock()
        mocked_view_1.interval = 0
        mocked_view_1.show = Mock()
        mocked_view_2 = Mock()
        mocked_view_2.interval = 0
        mocked_view_2.show = Mock()
        mocked_view_3 = Mock()
        mocked_view_3.interval = 0
        mocked_view_3.show = Mock()

        views = [mocked_view_1, mocked_view_2, mocked_view_3]
        view_manager = ViewManager(views, mocked_epd)

        view_manager.start()
        time.sleep(0.1)
        view_manager.next()
        time.sleep(0.1)
        view_manager.stop()
        view_manager.join()

        assert mocked_view_1.show.called
        assert mocked_view_2.show.called
        assert not mocked_view_3.show.called
        assert view_manager.current_view == 1

    def test_run_with_prev_action(self, mocker):
        mocked_epd = Mock()
        mocked_epd.init = Mock()
        mocked_epd.Clear = Mock()
        mocked_view_1 = Mock()
        mocked_view_1.interval = 0
        mocked_view_1.show = Mock()
        mocked_view_2 = Mock()
        mocked_view_2.interval = 0
        mocked_view_2.show = Mock()
        mocked_view_3 = Mock()
        mocked_view_3.interval = 0
        mocked_view_3.show = Mock()

        views = [mocked_view_1, mocked_view_2, mocked_view_3]
        view_manager = ViewManager(views, mocked_epd)

        view_manager.start()
        time.sleep(0.1)
        view_manager.prev()
        time.sleep(0.1)
        view_manager.stop()
        view_manager.join()

        assert mocked_view_1.show.called
        assert not mocked_view_2.show.called
        assert mocked_view_3.show.called
        assert view_manager.current_view == 2

    def test_run_with_interval(self, mocker):
        mocked_epd = Mock()
        mocked_epd.init = Mock()
        mocked_epd.Clear = Mock()
        mocked_view_1 = Mock()
        mocked_view_1.interval = 2
        mocked_view_1.show = Mock()
        mocked_view_2 = Mock()
        mocked_view_2.interval = 0
        mocked_view_2.show = Mock()

        views = [mocked_view_1, mocked_view_2]
        view_manager = ViewManager(views, mocked_epd)

        view_manager.start()
        time.sleep(5)
        view_manager.stop()
        view_manager.join()

        assert mocked_view_1.show.call_count == 3
        assert not mocked_view_2.show.called

    def test_run_with_interval_stopped(self, mocker):
        mocked_epd = Mock()
        mocked_epd.init = Mock()
        mocked_epd.Clear = Mock()
        mocked_view_1 = Mock()
        mocked_view_1.interval = 10
        mocked_view_1.show = Mock()
        mocked_view_2 = Mock()
        mocked_view_2.interval = 0
        mocked_view_2.show = Mock()

        views = [mocked_view_1, mocked_view_2]
        view_manager = ViewManager(views, mocked_epd)

        view_manager.start()
        time.sleep(0.1)
        view_manager.stop()
        view_manager.join()

        assert mocked_view_1.show.call_count == 1
        assert not mocked_view_2.show.called

    def test_run_with_interval_switched(self, mocker):
        mocked_epd = Mock()
        mocked_epd.init = Mock()
        mocked_epd.Clear = Mock()
        mocked_view_1 = Mock()
        mocked_view_1.interval = 10
        mocked_view_1.show = Mock()
        mocked_view_2 = Mock()
        mocked_view_2.interval = 0
        mocked_view_2.show = Mock()

        views = [mocked_view_1, mocked_view_2]
        view_manager = ViewManager(views, mocked_epd)

        view_manager.start()
        time.sleep(0.5)
        view_manager.next()
        time.sleep(0.5)
        view_manager.stop()
        view_manager.join()

        assert mocked_view_1.show.called
        assert mocked_view_2.show.called

    def test_epd_status(self, mocker):
        mocked_epd = Mock()
        mocked_view = Mock()
        mocked_view.busy = True
        mocked_view.timestamp = "2023-04-16, 12:00:00"

        views = [mocked_view]
        view_manager = ViewManager(views, mocked_epd)
        expected_status = {
            "epd_busy": True,
            "current_view": 0,
            "total_views": 1,
            "timestamp": "2023-04-16, 12:00:00",
        }

        status = view_manager.epd_status()
        assert status == expected_status

    def test_current_display(self, mocker):
        mocked_epd = Mock()
        mocked_view = Mock()
        mocked_view.image = Mock()

        views = [mocked_view]
        view_manager = ViewManager(views, mocked_epd)

        current_display = view_manager.current_display()
        assert current_display == mocked_view.image

    def test_current_view_details(self, mocker):
        mocked_epd = Mock()
        mocked_view = Mock()
        mocked_view.name = "Test view"
        mocked_view.view_angle = 90
        mocked_view.interval = 0
        mocked_view.busy = False
        mocked_view.timestamp = "2023-04-16, 12:00:00"

        views = [mocked_view]
        view_manager = ViewManager(views, mocked_epd)
        expected_details = {
            "current_view": 0,
            "name": "Test view",
            "view_angle": 90,
            "interval": 0,
            "timestamp": "2023-04-16, 12:00:00",
            "busy": False,
        }

        current_view_details = view_manager.current_view_details()
        assert current_view_details == expected_details
