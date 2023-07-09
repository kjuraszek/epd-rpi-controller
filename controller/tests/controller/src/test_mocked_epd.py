"""
View class tests
"""

import pytest
import datetime
from unittest.mock import Mock
from PIL import Image

import src.view
from src.view import View
from src.mocked_epd import MockedEPD

class TestMockedEPD:
    def test_Clear(self, mocker):
        mocked_epd = MockedEPD(100, 100)
        
        mocked_image = Mock()
        mocked_image.save = Mock()
        mocked_Image_new = Mock(return_value=mocked_image)
        
        mocker.patch('PIL.Image.new', mocked_Image_new)
        mocker.patch('PIL.Image.Image.save', mocked_image.save)
        mocker.patch('src.MockedEPD.getbuffer', Mock(return_value=mocked_image))
        mocker.patch('src.MockedEPD.display', Mock())

        mocked_epd.Clear(0)
        
        mocked_Image_new.assert_called_once_with('1', (100, 100), 0)
        mocked_epd.getbuffer.assert_called_once_with(mocked_image)
        mocked_epd.display.assert_called_once_with(mocked_image)

    def test_getbuffer(self, mocker):
        mocked_epd = MockedEPD(100, 100)
        
        mocked_image = Mock()
        
        assert mocked_epd.getbuffer(mocked_image) == mocked_image

    def test_display(self, mocker):
        mocked_epd = MockedEPD(100, 100)
        
        mocked_image = Mock()
        mocked_image.save = Mock()
        mocker.patch('PIL.Image.Image.save', mocked_image.save)
        
        mocked_epd.display(mocked_image)
        
        mocked_image.save.assert_called_once_with('mocked_epd.png')

    def test_display_custom_filename(self, mocker):
        mocked_epd = MockedEPD(100, 100)
        custom_filename = 'custom_filename.png'
        
        mocked_image = Mock()
        mocked_image.save = Mock()
        mocker.patch('PIL.Image.Image.save', mocked_image.save)
        
        mocked_epd.display(mocked_image, custom_filename)
        
        mocked_image.save.assert_called_once_with(custom_filename)
