"""
View class tests
"""

import pytest
import datetime
from unittest.mock import Mock
from PIL import Image

import src.view
from src.view import View

class TestView:
    def test_show(self, mocker):
        view = View('test_view', 0)

        mocker.patch('src.View._after_epd_change', Mock())

        with pytest.raises(NotImplementedError):
            view.show(first_call=True)

        assert not view._after_epd_change.called

    def test_show_mocked_epd_change(self, mocker):
        view = View('test_view', 0)

        mocker.patch('src.View._before_epd_change', Mock())
        mocker.patch('src.View._epd_change', Mock())
        mocker.patch('src.View._set_timestamp', Mock())

        view.show(False)

        assert view._before_epd_change.called
        view._epd_change.assert_called_once_with(False)
        assert view._set_timestamp.called

    def test_before_epd_change(self, mocker):
        view = View('test_view', 0)

        assert not view.busy
        view._before_epd_change()
        assert view.busy

    def test_epd_change(self, mocker):
        view = View('test_view', 0)

        with pytest.raises(NotImplementedError):
            view._epd_change(first_call=True)

    def test_after_epd_change(self, mocker):
        view = View('test_view', 0)

        mocker.patch('src.View._set_timestamp', Mock())

        view._after_epd_change()
        assert view._set_timestamp.called

    def test_rotate_image_no_image(self, mocker):
        view = View('test_view', 0)
        view.image = None

        view._rotate_image()
        assert not view.image

        mock = Mock()
        mock.rotate = Mock()
        view.image = mock

        view._rotate_image()
        assert view.image == mock
        assert not mock.rotate.called

    def test_rotate_image_mocked_image(self, mocker):
        view = View('test_view', 0, 180)
        assert view.view_angle == 180

        old_image = Mock(spec=Image.Image)
        new_image = Mock(spec=Image.Image)
        old_image.rotate = Mock(return_value=new_image)
        new_image.rotate = Mock()
        view.image = old_image

        view._rotate_image()

        assert old_image != new_image
        assert view.image == new_image
        assert not new_image.rotate.called
        old_image.rotate.assert_called_once_with(180)

    def test_set_timestamp(self, mocker):
        view = View('test_view', 0)
        assert not view.timestamp

        date_time = datetime.datetime(2023, 3, 23, 12, 40, 30, 0)
        timestamp = "2023-03-23, 12:40:30"

        mock_date = Mock()
        mock_date.now.return_value = date_time
        mock_date.strftime.return_value = timestamp

        mocker.patch('src.view.datetime', mock_date)

        view._set_timestamp()

        assert src.view.datetime.now() == date_time
        assert view.timestamp == timestamp

    def test_fallback(self, mocker):
        view = View('test_view', 0)
        with pytest.raises(NotImplementedError):
            view._fallback()

    def test_conditional(self, mocker):
        view = View('test_view', 0)
        assert view._conditional() == True
