"""
Application class tests
"""

from tornado.testing import AsyncHTTPTestCase
from unittest.mock import Mock, patch

from PIL import Image

from src.api.application import TornadoApplication

class TestApplication:
    @patch('src.api.application.setup_swagger')
    def test_app(self, setup_swagger_mock):
        mocked_view_manager = Mock()

        app = TornadoApplication(mocked_view_manager)

        assert len(app._api_routes) == 4
        assert len(app._routes) == 1
        assert setup_swagger_mock.called

class TestApplicationRoutes(AsyncHTTPTestCase):
    def get_app(self):
        mocked_image = Mock(spec=Image.Image)
        mocked_image.rotate = Mock(return_value=mocked_image)

        mocked_view_manager = Mock()
        mocked_view_manager.epd_status = Mock(return_value={})
        mocked_view_manager.next = Mock()
        mocked_view_manager.prev = Mock()
        mocked_view_manager.busy.is_set = Mock(return_value=False)        
        mocked_view_manager.current_display = Mock(return_value=mocked_image)
        mocked_view_manager.current_view_details = Mock(return_value={})
        
        self.app = TornadoApplication(mocked_view_manager)
        return self.app

    def test_routes(self):
        success_routes = ['/', '/api/status','/api/current_display']
        no_content_routes = ['/api/next', '/api/prev']
        not_found_routes = ['/not_found', '/test']
        
        for route in success_routes:
            response = self.fetch(route, method='GET')
            assert response.code == 200
        for route in no_content_routes:
            response = self.fetch(route, method='GET')
            assert response.code == 204
        for route in not_found_routes:
            response = self.fetch(route, method='GET')
            assert response.code == 404
