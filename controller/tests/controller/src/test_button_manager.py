"""
ButtonManager class tests
"""

import sys
import pytest
import importlib
import time
from unittest.mock import Mock

import src.button_manager
from src.button_manager import ButtonManager


class TestButtonManagerImports:
    def test_import_mock_gpio(self, mocker):
        from src.button_manager import ButtonManager

        importlib.reload(src.button_manager)
        assert sys.modules["Mock.GPIO"]
        assert not "RPi" in sys.modules
        del sys.modules["Mock"]

    def test_import_rpi_gpio(self, mocker):
        mocker.patch("config.Config.USE_BUTTONS", True)

        from src.button_manager import ButtonManager

        with pytest.raises(RuntimeError):
            importlib.reload(src.button_manager)
            # raising RuntimeError for compatibility with running tests on RPi devices
            raise RuntimeError

        assert sys.modules["RPi"]
        assert not "Mock" in sys.modules
        del sys.modules["RPi"]


class TestButtonManager:
    def test_stop(self, mocker):
        button_manager = ButtonManager()
        button_manager.stop_event = Mock()
        button_manager.stop_event.set = Mock()

        button_manager.stop()
        button_manager.stop_event.set.assert_called_once()

    def test_run(self, mocker):
        mocked_kafka_producer = Mock()
        mocked_kafka_producer.send = Mock()
        mocked_kafka_producer.close = Mock()
        mock = Mock(return_value=mocked_kafka_producer)

        mocked_gpio = Mock()
        mocked_gpio.add_event_detect = Mock()
        mocker.patch("src.button_manager.KafkaProducer", mock)
        mocker.patch("src.button_manager.GPIO", mocked_gpio)
        button_manager = ButtonManager()

        button_manager.start()
        time.sleep(1)
        button_manager.stop()
        button_manager.join()

        assert mocked_gpio.add_event_detect.call_count == 2
        assert mocked_kafka_producer.close.call_count == 1

    def test_left_button_callback(self, mocker):
        mocked_kafka_producer = Mock()
        mocked_kafka_producer.send = Mock()
        mock = Mock(return_value=mocked_kafka_producer)

        mocker.patch("src.button_manager.KafkaProducer", mock)

        button_manager = ButtonManager()
        button_manager._left_button_callback()

        assert not mocked_kafka_producer.send.called

        button_manager.producer = mocked_kafka_producer
        button_manager._left_button_callback()

        mocked_kafka_producer.send.assert_called_once_with(
            "epd_rpi_view_manager_tests", bytes("prev", encoding="utf-8")
        )

    def test_right_button_callback(self, mocker):
        mocked_kafka_producer = Mock()
        mocked_kafka_producer.send = Mock()
        mock = Mock(return_value=mocked_kafka_producer)

        mocker.patch("src.button_manager.KafkaProducer", mock)

        button_manager = ButtonManager()
        button_manager._right_button_callback()

        assert not mocked_kafka_producer.send.called

        button_manager.producer = mocked_kafka_producer
        button_manager._right_button_callback()

        mocked_kafka_producer.send.assert_called_once_with(
            "epd_rpi_view_manager_tests", bytes("next", encoding="utf-8")
        )
