"""Module exports ViewManager class"""

import threading
from typing import Any, Optional, Sequence

from waiting import wait, TimeoutExpired
from PIL import Image

from config import Config
from logger import logger
from src.helpers import BaseThread
from src.view import View


class ViewManager(BaseThread):
    """View manager controls views

    ViewManager is reponsible for switching views. Also it returns EPD's current status.
    """

    def __init__(self, views: Sequence[View], epd: Any) -> None:
        """ViewManager constructor method"""
        BaseThread.__init__(self)
        self.busy = threading.Event()
        self.current_view = Config.STARTING_VIEW
        self.views = views
        self.action: Optional[str] = None
        self.epd = epd
        self.timestamp: Optional[str] = None

    def next(self) -> None:
        """Method triggers next view if manager isn't busy"""
        if not self.busy.is_set():
            self.busy.set()
            self.action = 'next'
        else:
            logger.debug('View manager is busy')

    def prev(self) -> None:
        """Method triggers previous view if manager isn't busy"""
        if not self.busy.is_set():
            self.busy.set()
            self.action = 'prev'
        else:
            logger.debug('View manager is busy')

    def stop(self) -> None:
        """Method stops the ViewManager"""
        self.stop_event.set()

    def run(self) -> None:
        """Main method which runs on manager start

        Method switches between views and stops the controller on certain actions.
        Method is also responsible for triggering show method of current View.
        """

        switched = False
        first_call = True
        self.epd.init(0)
        self.epd.Clear(0xFF)
        while not self.stop_event.is_set():
            if self.busy.is_set() and self.action in ('next', 'prev'):
                if self.action == 'next':
                    self.current_view = self.current_view + 1 if self.current_view < len(self.views) - 1 else 0
                else:
                    self.current_view = self.current_view - 1 if self.current_view > 0 else len(self.views) - 1
                switched = False
                first_call = True
            if not switched:
                self.busy.set()
                logger.debug('\tView is running')
                self.views[self.current_view].show(first_call=first_call)
                logger.debug('\tView is idle')
                self.busy.clear()
                if self.views[self.current_view].interval == 0:
                    switched = True
                else:
                    first_call = False
                    switched = False
                    try:
                        wait(lambda: self.busy.is_set() or self.stop_event.is_set(),
                             timeout_seconds=self.views[self.current_view].interval)
                    except TimeoutExpired:
                        continue
                    else:
                        if self.stop_event.is_set():
                            break
                        if self.busy.is_set():
                            continue

    def epd_status(self) -> dict[str, Any]:
        """Method returns EPD's current status"""
        return {
            'epd_busy': self.views[self.current_view].busy,
            'current_view': self.current_view,
            'total_views': len(self.views),
            'timestamp': self.views[self.current_view].timestamp
        }

    def current_display(self) -> Optional[Image.Image]:
        """Method returns EPD's currently displayed image"""
        return self.views[self.current_view].image

    def current_view_details(self) -> dict[str, Any]:
        """Method returns EPD's currently displayed image"""
        details = {
            'current_view': self.current_view,
            'name': self.views[self.current_view].name,
            'view_angle': self.views[self.current_view].view_angle,
            'interval': self.views[self.current_view].interval,
            'timestamp': self.views[self.current_view].timestamp,
            'busy': self.views[self.current_view].busy,
        }
        return details
