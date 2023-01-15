import threading
import logging
from datetime import datetime

from waiting import wait, TimeoutExpired

from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ViewManager(threading.Thread):
    '''
    view manager
    '''
    def __init__(self, views, epd):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.busy = threading.Event()
        self.current_view = Config.STARTING_VIEW
        self.views = views
        self.action = None
        self.epd = epd
        self.timestamp = None

    def next(self):
        if not self.busy.is_set():
            self.busy.set()
            self.action = 'next'
        else:
            logger.debug('View manager is busy')

    def prev(self):
        if not self.busy.is_set():
            self.busy.set()
            self.action = 'prev'
        else:
            logger.debug('View manager is busy')

    def stop(self):
        self.stop_event.set()

    def run(self):
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
                self.views[self.current_view].show(first_call = first_call)
                self._set_timestamp()
                logger.debug('\tView is idle')
                self.busy.clear()
                if self.views[self.current_view].interval == 0:
                    switched = True
                else:
                    first_call = False
                    switched = False
                    try:
                        wait(lambda : self.busy.is_set() or self.stop_event.is_set(),
                             timeout_seconds=self.views[self.current_view].interval)
                    except TimeoutExpired:
                        continue
                    else:
                        if self.stop_event.is_set():
                            break
                        if self.busy.is_set():
                            continue

    def epd_status(self):
        return {
            'epd_busy': self.busy.is_set(),
            'current_view': self.current_view,
            'total_views': len(self.views),
            'timestamp': self.timestamp
        }

    def current_display(self):
        return self.views[self.current_view].image

    def _set_timestamp(self):
        current_date = datetime.now()
        self.timestamp = current_date.strftime("%Y-%m-%d, %H:%M:%S")
