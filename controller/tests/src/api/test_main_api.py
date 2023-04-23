"""
Main API class tests
"""

from unittest.mock import Mock

from src.api.main_api import MainAPI

class TestMainAPI:
    def test_stop(self, mocker):
        mocked_view_manager = Mock()
        main_api = MainAPI(mocked_view_manager)
        main_api.ioloop = Mock()
        main_api.ioloop.add_callback = Mock()
        main_api.http_server = Mock()
        main_api.http_server.stop = Mock()

        main_api.stop()
        main_api.ioloop.add_callback.assert_called_once()
        main_api.http_server.stop.assert_called_once()

    def test_run(self, mocker):
        mocked_view_manager = Mock()
        mocked_asyncio = Mock()
        mocked_asyncio.set_event_loop = Mock()
        mocked_asyncio.new_event_loop = Mock()
        mocked_ioloop = Mock()
        mocked_ioloop.current = Mock()
        mocked_ioloop.start = Mock()
        
        mocked_http_server_instance = Mock()
        mocked_http_server_instance.listen = Mock()
        mocked_http_server = Mock(return_value=mocked_http_server_instance)
        
        mocker.patch('src.api.main_api.asyncio', mocked_asyncio)
        mocker.patch('tornado.ioloop.IOLoop', mocked_ioloop)
        mocker.patch('tornado.httpserver.HTTPServer', mocked_http_server)

        main_api = MainAPI(mocked_view_manager)
        main_api.run()      

        mocked_asyncio.set_event_loop.assert_called_once
        mocked_asyncio.new_event_loop.assert_called_once
        mocked_http_server_instance.listen.assert_called_once_with(50000)
        mocked_ioloop.current.assert_called_once
        mocked_ioloop.start.assert_called_once
