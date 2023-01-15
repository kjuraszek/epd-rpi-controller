"""Module exports ViewManager class"""

import threading
import logging
from datetime import datetime

from waiting import wait, TimeoutExpired

from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ViewManager(threading.Thread):
    """View manager controls views

    ViewManager is reponsible for switching views. Also it returns EPD's current status.
    """

    def __init__(self, views, epd):
        """ViewManager constructor method"""
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.busy = threading.Event()
        self.current_view = Config.STARTING_VIEW
        self.views = views
        self.action = None
        self.epd = epd
        self.timestamp = None

    def next(self):
        """Method triggers next view if manager isn't busy"""
        if not self.busy.is_set():
            self.busy.set()
            self.action = 'next'
        else:
            logger.debug('View manager is busy')

    def prev(self):
        """Method triggers previous view if manager isn't busy"""
        if not self.busy.is_set():
            self.busy.set()
            self.action = 'prev'
        else:
            logger.debug('View manager is busy')

    def stop(self):
        """Method stops the ViewManager"""
        self.stop_event.set()

    def run(self):
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
                self._set_timestamp()
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

    def epd_status(self):
        """Method returns EPD's current status"""
        return {
            'epd_busy': self.busy.is_set(),
            'current_view': self.current_view,
            'total_views': len(self.views),
            'timestamp': self.timestamp
        }

    def current_display(self):
        """Method returns EPD's currently displayed image"""
        return self.views[self.current_view].image

    def _set_timestamp(self):
        """Method sets a timestamp"""
        current_date = datetime.now()
        self.timestamp = current_date.strftime("%Y-%m-%d, %H:%M:%S")
