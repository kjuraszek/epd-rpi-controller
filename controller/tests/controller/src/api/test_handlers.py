"""
Request handlers tests
"""

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from unittest.mock import Mock

from PIL import Image

from src.api.handlers import BaseHandler, RootHandler, StatusHandler, NextViewHandler, PreviousViewHandler, CurrentDisplayHandler

class TestBaseHandler(AsyncHTTPTestCase):
    def get_app(self) -> Application:
        self.app = Application([('/', BaseHandler)])
        return self.app

    def test_get(self):
        response = self.fetch('/', method='GET')
        expected_headers = {'Access-Control-Allow-Origin': '*',
                           'Access-Control-Allow-Headers': 'x-requested-with',
                           'Access-Control-Allow-Methods': 'GET'}
        
        self.assertEqual(405, response.code)
        for header in expected_headers:
            assert response.headers[header] == expected_headers[header]


class TestRootHandler(AsyncHTTPTestCase):
    def get_app(self) -> Application:
        self.app = Application([('/', RootHandler)])
        return self.app

    def test_get(self):
        expected_body = b'EPD RPI Controller\'s API root'
        response = self.fetch('/', method='GET')
        
        assert 200 == response.code
        assert expected_body == response.body


class TestStatusHandler(AsyncHTTPTestCase):
    def get_app(self) -> Application:
        mocked_view_manager = Mock()
        mocked_view_manager.epd_status = Mock(return_value={'status': 'test_status'})
        self.app = Application([('/', StatusHandler, dict(view_manager=mocked_view_manager))])
        return self.app

    def test_get(self):
        expected_body = b'{"status": "test_status"}'
        response = self.fetch('/', method='GET')
        
        assert 200 == response.code
        assert expected_body == response.body


class TestNextViewHandler(AsyncHTTPTestCase):
    def get_app(self) -> Application:
        self.mocked_view_manager = Mock()
        self.mocked_view_manager.next = Mock()
        self.mocked_view_manager.prev = Mock()
        self.app = Application([('/', NextViewHandler, dict(view_manager=self.mocked_view_manager))])
        return self.app

    def test_get(self):
        self.mocked_view_manager.busy.is_set = Mock(return_value=False)
        expected_body = b''
        response = self.fetch('/', method='GET')

        assert 204 == response.code
        assert expected_body == response.body
        assert self.mocked_view_manager.next.called
        assert not self.mocked_view_manager.prev.called

    def test_get_busy(self):
        self.mocked_view_manager.busy.is_set = Mock(return_value=True)
        expected_body = b''
        response = self.fetch('/', method='GET')

        assert 400 == response.code
        assert expected_body == response.body
        assert not self.mocked_view_manager.next.called
        assert not self.mocked_view_manager.prev.called


class TestPreviousViewHandler(AsyncHTTPTestCase):
    def get_app(self) -> Application:
        self.mocked_view_manager = Mock()
        self.mocked_view_manager.next = Mock()
        self.mocked_view_manager.prev = Mock()
        self.app = Application([('/', PreviousViewHandler, dict(view_manager=self.mocked_view_manager))])
        return self.app

    def test_get(self):
        self.mocked_view_manager.busy.is_set = Mock(return_value=False)
        expected_body = b''
        response = self.fetch('/', method='GET')

        assert 204 == response.code
        assert expected_body == response.body
        assert not self.mocked_view_manager.next.called
        assert self.mocked_view_manager.prev.called

    def test_get_busy(self):
        self.mocked_view_manager.busy.is_set = Mock(return_value=True)
        expected_body = b''
        response = self.fetch('/', method='GET')

        assert 400 == response.code
        assert expected_body == response.body
        assert not self.mocked_view_manager.next.called
        assert not self.mocked_view_manager.prev.called


class TestCurrentDisplayHandler(AsyncHTTPTestCase):
    def get_app(self) -> Application:
        self.mocked_view_manager = Mock()
        self.app = Application([('/', CurrentDisplayHandler, dict(view_manager=self.mocked_view_manager))])
        return self.app

    def test_get(self):
        mocked_image = Mock(spec=Image.Image)
        mocked_image.rotate = Mock(return_value=mocked_image)
        
        self.mocked_view_manager.current_display = Mock(return_value=mocked_image)
        self.mocked_view_manager.current_view_details = Mock(return_value={})
        expected_body = b''
        expected_headers = {
            'Content-type': 'image/jpg',
            'Content-length': '0'
        }
        response = self.fetch('/', method='GET')

        assert 200 == response.code
        assert expected_body == response.body
        for header in expected_headers:
            assert response.headers[header] == expected_headers[header]
        mocked_image.rotate.assert_called_once_with(0)
        assert mocked_image.save.called

    def test_get_without_image(self):
        self.mocked_view_manager.current_display = Mock(return_value='not an image')
        expected_body = b''
        response = self.fetch('/', method='GET')

        assert 400 == response.code
        assert expected_body == response.body

    def test_get_with_details(self):
        mocked_rotated_image = Mock(spec=Image.Image)
        mocked_rotated_image.save = Mock()
        mocked_image = Mock(spec=Image.Image)
        mocked_image.rotate = Mock(return_value=mocked_rotated_image)
        
        self.mocked_view_manager.current_display = Mock(return_value=mocked_image)
        self.mocked_view_manager.current_view_details = Mock(return_value={'view_angle': 90})
        expected_body = b''
        expected_headers = {
            'Content-type': 'image/jpg',
            'Content-length': '0'
        }
        response = self.fetch('/', method='GET')

        assert 200 == response.code
        assert expected_body == response.body
        for header in expected_headers:
            assert response.headers[header] == expected_headers[header]
        mocked_image.rotate.assert_called_once_with(-90)
        assert mocked_rotated_image.save.called
