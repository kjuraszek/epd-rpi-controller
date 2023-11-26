"""
helpers tests
"""

import pytest
from unittest.mock import Mock
from PIL import ImageFont
from src.helpers import (
    BaseThread,
    WrappedTitle,
    signal_handler,
    wrap_text,
    wrap_titles,
    view_conditional,
    view_fallback,
)


class TestHelpers:
    def test_base_thread(self, mocker):
        thread = BaseThread()
        assert not thread.stop_event.is_set()

        with pytest.raises(NotImplementedError):
            thread.stop()

    def test_signal_handler(self, mocker):
        thread = BaseThread()
        assert not thread.stop_event.is_set()

        signal_handler(thread, (2,))
        assert thread.stop_event.is_set()

    def test_view_fallback(self, mocker):
        @view_fallback
        def mocked_function(arg):
            pass

        @view_fallback
        def mocked_function_raising_exception(arg):
            raise Exception

        mocked_view_object = Mock()

        mocked_function(mocked_view_object)
        assert not mocked_view_object._fallback.called

        mocked_function_raising_exception(mocked_view_object)
        assert mocked_view_object._fallback.called

    def test_view_conditional(self, mocker):
        mocked_function = Mock()
        mocked_function_second = Mock()
        mocked_view_object = Mock()

        mocked_view_object._conditional.return_value = True
        view_conditional(mocked_function)(mocked_view_object)
        assert mocked_function.called

        mocked_view_object._conditional.return_value = False
        view_conditional(mocked_function_second)(mocked_view_object)
        assert not mocked_function_second.called

    def test_wrap_text(self, mocker):
        font = ImageFont.load_default()

        with pytest.raises(ValueError):
            wrapped_text = wrap_text(1, 100, font, "Lorem testum testum")

        with pytest.raises(ValueError):
            wrapped_text = wrap_text(100, 1, font, "Lorem testum testum")

        wrapped_text = wrap_text(200, 60, font, "Lorem testum testum")
        assert wrapped_text == "Lorem testum testum"

        wrapped_text = wrap_text(20, 60, font, "Lorem testum testum")
        assert wrapped_text == "Lor\nem \ntes\ntum\n te\nstum"

    def test_wrap_titles(self, mocker):
        font = ImageFont.load_default()

        wrapped_titles = wrap_titles(200, 200, font, [])
        assert wrapped_titles == []

        wrapped_titles = wrap_titles(200, 200, font, ["Lorem testum testum"])
        assert len(wrapped_titles) == 1
        assert isinstance(wrapped_titles[0], WrappedTitle)
        assert wrapped_titles[0].text_height == 11
        assert wrapped_titles[0].text_width == 114
        assert wrapped_titles[0].wrapped_text == "Lorem testum testum"

        wrapped_titles = wrap_titles(
            100, 100, font, ["Lorem testum testum", "Lorem second testum testum"]
        )
        assert len(wrapped_titles) == 2
        assert isinstance(wrapped_titles[1], WrappedTitle)
        assert wrapped_titles[1].text_height == 26
        assert wrapped_titles[1].text_width == 96
        assert wrapped_titles[1].wrapped_text == "Lorem second tes\ntum testum"
