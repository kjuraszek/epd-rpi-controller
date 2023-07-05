"""
AirPollution view class
"""

import os
from typing import Any, Union

from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import requests
from requests.adapters import HTTPAdapter, Retry

from custom_views.examplary_views.base_view import BaseView
from logger import logger
from src.helpers import view_fallback, wrap_titles


# pylint: disable=R0801
class AirPollutionView(BaseView):
    '''
    View is displaying current air pollution: AQI and other related parameters gathered from OpenWeather API.

    It uses environment variables to prepare connection URL.
    '''
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        load_dotenv()
        weather_key = os.getenv('WEATHER_KEY')
        weather_lat = os.getenv('WEATHER_LAT')
        weather_lon = os.getenv('WEATHER_LON')
        if None in (weather_key, weather_lat, weather_lon):
            self.url = None
        else:
            self.url = f'https://api.openweathermap.org/data/2.5/air_pollution?lat={weather_lat}&lon={weather_lon}&appid={weather_key}'
        self.air_data: dict[str, Union[int, float]] = {}
        self.icons = ('\uf118', '\uf118', '\uf11a', '\uf119', '\uf119')

    # pylint: disable=R0914
    @view_fallback
    def _epd_change(self, first_call: bool) -> None:
        '''
        IMPORTANT!

        Below positions of text and font sizes are chosen arbitrary and they are adjusted to 200x200 EPD, adjust them to your needs!
        Also - units are metrical.
        '''
        logger.info('%s is running', self.name)

        image = Image.new('1', (self.epd.width, self.epd.height), 255)

        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Impact.ttf', 22)
        font_large = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Impact.ttf', 32)
        font_awesome = ImageFont.truetype('/usr/share/fonts/truetype/font-awesome/fontawesome-webfont.ttf', 32)

        aqi = self.air_data.get('aqi')
        if aqi not in range(1, 6):
            aqi_label = 'AQI:  N/A'
            aqi = 5
        else:
            aqi_label = f'AQI:  {aqi} / 5'

        _, _, aqi_label_width, aqi_label_height = draw.multiline_textbbox((0, 0), aqi_label, font_large)

        draw.text((0, 0), aqi_label, font=font_large, fill=0)
        draw.text((aqi_label_width + 5, 5), self.icons[aqi - 1], font=font_awesome, fill=0)  # type: ignore

        margin_top = aqi_label_height + 5
        column_width = self.epd.width//2

        titles = [f'{key.upper()}: {value}' for key, value in self.air_data.items() if value is not None and key != 'aqi']
        wrapped_data = wrap_titles(column_width, self.epd.height, font, titles)

        current_height = margin_top
        current_width = 0

        for data in wrapped_data:
            draw.text((current_width, current_height), data.wrapped_text, font=font, fill=0)
            current_height += data.text_height + 4
            if current_height > self.epd.height - 30:
                current_height = margin_top
                current_width = column_width

        self.image = image
        self._rotate_image()
        self.epd.display(self.epd.getbuffer(self.image))

    def _get_data(self) -> dict[str, Any]:
        if not self.url:
            logger.error('URL not created, serving fallback image!')
            raise ValueError
        try:
            session = requests.Session()
            retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
            session.mount('http://', HTTPAdapter(max_retries=retries))
            session.mount('https://', HTTPAdapter(max_retries=retries))

            data = session.get(self.url).json()
            data_list = data.get('list', [])
            air_data = {}
            if len(data_list) > 0:
                air_data['aqi'] = int(data_list[0].get('main', {}).get('aqi'))
                air_data['co'] = round(data_list[0].get('components', {}).get('co'), 2)
                air_data['no'] = round(data_list[0].get('components', {}).get('no'), 2)
                air_data['no2'] = round(data_list[0].get('components', {}).get('no2'), 2)
                air_data['o3'] = round(data_list[0].get('components', {}).get('o3'), 2)
                air_data['so2'] = round(data_list[0].get('components', {}).get('so2'), 2)
                air_data['pm2.5'] = round(data_list[0].get('components', {}).get('pm2_5'), 2)
                air_data['pm10'] = round(data_list[0].get('components', {}).get('pm10'), 2)
                air_data['nh3'] = round(data_list[0].get('components', {}).get('nh3'), 2)
            return air_data
        except Exception:  # pylint: disable=W0703
            logger.error('Unable to collect the data from OpenWeather API.')
            return {}

    def _conditional(self, *args: Any, **kwargs: Any) -> bool:
        air_data = self._get_data()
        if not air_data:
            return False
        if bool(kwargs['first_call']) or air_data != self.air_data:
            self.air_data = air_data
            return True
        return False
