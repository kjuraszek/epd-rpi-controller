"""Module exports MainAPI class"""

import logging
import asyncio

import tornado.ioloop
import tornado.web
import tornado.httpserver

from config import Config
from src.helpers import BaseThread
from src.view_manager import ViewManager
from .application import TornadoApplication

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MainAPI(BaseThread):
    """API used in UI accessed in browser"""

    def __init__(self, view_manager: ViewManager) -> None:
        """MainAPI constructor method"""
        BaseThread.__init__(self, daemon=True)
        self.view_manager = view_manager
        self.http_server: tornado.httpserver.HTTPServer
        self.ioloop: tornado.ioloop.IOLoop

        self.app = TornadoApplication(self.view_manager)

    def run(self) -> None:
        """Main method which runs on Consumer start

        Method starts the tornado server and listens on a certain port.
        """

        logger.info('Starting tornado server')
        asyncio.set_event_loop(asyncio.new_event_loop())

        self.http_server = tornado.httpserver.HTTPServer(self.app)
        self.http_server.listen(Config.VITE_API_PORT)

        self.ioloop = tornado.ioloop.IOLoop.current()
        logger.info('Serving swagger at http://localhost:%s/api/doc/', Config.VITE_API_PORT)
        self.ioloop.start()

        logger.info('Tornado server has been stopped')

    def stop(self) -> None:
        """Method stops the MainAPI"""
        logger.info('Stopping tornado server')
        self.http_server.stop()
        self.ioloop.add_callback(self.ioloop.stop)
