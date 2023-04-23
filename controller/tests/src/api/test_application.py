"""
Application class tests
"""

from unittest.mock import Mock, patch

from src.api.application import TornadoApplication

class TestApplication:
    @patch('src.api.application.setup_swagger')
    def test_app(self, setup_swagger_mock):
        mocked_view_manager = Mock()

        app = TornadoApplication(mocked_view_manager)

        assert len(app._api_routes) == 4
        assert len(app._routes) == 1
        assert setup_swagger_mock.called
