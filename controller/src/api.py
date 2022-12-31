import threading
import logging
import asyncio

import tornado.ioloop
import tornado.web
import tornado.httpserver


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MainAPI(threading.Thread):
    def __init__(self, view_manager):
        threading.Thread.__init__(self, daemon=True)
        self.view_manager = view_manager
        self.http_server = None
        self.ioloop = None
        HANDLERS = [
            (r"/", RootHandler),
        ]
        self.app = tornado.web.Application(
            handlers=HANDLERS
        )
        
    def run(self):        
        logger.info('Starting tornado server')
        asyncio.set_event_loop(asyncio.new_event_loop())
        
        self.http_server = tornado.httpserver.HTTPServer(self.app)
        self.http_server.listen(8888)

        self.ioloop = tornado.ioloop.IOLoop.current()
        self.ioloop.start()
        
        logger.info('Tornado server has been stopped')

    def stop(self):
        logger.info('Stopping tornado server')
        self.http_server.stop()
        self.ioloop.add_callback(self.ioloop.stop)


class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("EPD RPI Controller's API root")

