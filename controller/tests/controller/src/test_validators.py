"""
validators tests
"""

import pytest
from src.validators import validate_views, validate_config, ValidationViewException, ValidationConfigException
from custom_views.examplary_views import DummyView


class TestValidateConfig:
    def test_validate_config(self, mocker):
        validate_config()

    def test_validate_config_kafka_topic(self, mocker):
        mocker.patch("config.Config.KAFKA_VIEW_MANAGER_TOPIC", None)
        with pytest.raises(ValidationConfigException):
            validate_config()

        mocker.patch("config.Config.KAFKA_VIEW_MANAGER_TOPIC", 111)
        with pytest.raises(ValidationConfigException):
            validate_config()

        mocker.patch("config.Config.KAFKA_VIEW_MANAGER_TOPIC", 'test-topic')
        validate_config()

    def test_validate_config_starting_view(self, mocker):
        mocked_views = [DummyView('test_name', 0, 0)]
        mocker.patch("src.validators.VIEWS", mocked_views)

        mocker.patch("config.Config.STARTING_VIEW", -1)
        with pytest.raises(ValidationConfigException):
            validate_config()

        mocker.patch("config.Config.STARTING_VIEW", 111)
        with pytest.raises(ValidationConfigException):
            validate_config()

        mocker.patch("config.Config.STARTING_VIEW", 0)
        validate_config()

    def test_validate_config_epd_model(self, mocker):
        mocker.patch("config.Config.EPD_MODEL", "mock")

        mocker.patch("config.Config.MOCKED_EPD_WIDTH", None)
        with pytest.raises(ValidationConfigException):
            validate_config()

        mocker.patch("config.Config.MOCKED_EPD_WIDTH", 0)
        with pytest.raises(ValidationConfigException):
            validate_config()

        mocker.patch("config.Config.MOCKED_EPD_WIDTH", 10)
        validate_config()

        mocker.patch("config.Config.MOCKED_EPD_HEIGHT", "123")
        with pytest.raises(ValidationConfigException):
            validate_config()

        mocker.patch("config.Config.MOCKED_EPD_HEIGHT", -10)
        with pytest.raises(ValidationConfigException):
            validate_config()

        mocker.patch("config.Config.MOCKED_EPD_HEIGHT", 10)
        validate_config()

    def test_validate_config_use_buttons(self, mocker):
        mocker.patch("config.Config.USE_BUTTONS", True)
        mocker.patch("config.Config.RIGHT_BUTTON_PIN", 12)

        mocker.patch("config.Config.LEFT_BUTTON_PIN", None)
        with pytest.raises(ValidationConfigException):
            validate_config()

        mocker.patch("config.Config.LEFT_BUTTON_PIN", 0)
        with pytest.raises(ValidationConfigException):
            validate_config()

        mocker.patch("config.Config.LEFT_BUTTON_PIN", 10)
        validate_config()

        mocker.patch("config.Config.RIGHT_BUTTON_PIN", "123")
        with pytest.raises(ValidationConfigException):
            validate_config()

        mocker.patch("config.Config.RIGHT_BUTTON_PIN", -10)
        with pytest.raises(ValidationConfigException):
            validate_config()

        mocker.patch("config.Config.RIGHT_BUTTON_PIN", 10)
        with pytest.raises(ValidationConfigException):
            validate_config()

        mocker.patch("config.Config.RIGHT_BUTTON_PIN", 11)
        validate_config()


class TestValidateViews:
    def test_validate_views(self, mocker):
        mocked_views = [DummyView('test_name', 0, 0)]
        mocker.patch("src.validators.VIEWS", mocked_views)
        validate_views()

    def test_validate_views_empty(self, mocker):
        mocked_views = []
        mocker.patch("src.validators.VIEWS", mocked_views)
        with pytest.raises(ValidationViewException):
            validate_views()

    def test_validate_views_mixed_elements(self, mocker):
        mocked_views = [DummyView('test_name', 0, 0), 1, 'test', ]
        mocker.patch("src.validators.VIEWS", mocked_views)
        with pytest.raises(ValidationViewException):
            validate_views()
