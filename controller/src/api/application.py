"""Module exports TornadoApplication"""

import tornado.web

from tornado_swagger.setup import setup_swagger

from src.view_manager import ViewManager
from .handlers import RootHandler, StatusHandler, NextViewHandler, PreviousViewHandler, CurrentDisplayHandler


class TornadoApplication(tornado.web.Application):
    """TornadoApplication is an API for EPD RPI Controller"""
    def __init__(self, view_manager: ViewManager):
        """TornadoApplication constructor method"""
        self._routes = [
            (r"/", RootHandler),
        ]
        self._api_routes = [
            tornado.web.url(r'/api/status', StatusHandler, dict(view_manager=view_manager)),
            tornado.web.url(r'/api/next', NextViewHandler, dict(view_manager=view_manager)),
            tornado.web.url(r'/api/prev', PreviousViewHandler, dict(view_manager=view_manager)),
            tornado.web.url(r'/api/current_display', CurrentDisplayHandler, dict(view_manager=view_manager)),
        ]
        setup_swagger(self._api_routes,
                      api_base_url='/',
                      description='API for EPD RPI Controller',
                      api_version='1.0.0',
                      title='EPD RPI Controller API',
                      schemes=['http'],
                      )
        super().__init__(self._routes + self._api_routes)  # type: ignore
