"""
AirPollution view class
"""

import logging
import os

from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import requests
from requests.adapters import HTTPAdapter, Retry

from custom_views.examplary_views.base_view import BaseView
from src.helpers import view_fallback, wrap_titles


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# pylint: disable=R0801
class AirPollutionView(BaseView):
    '''
    View is displaying current air pollution: AQI and other related parameters gathered from OpenWeather API.
    
    It uses environment variables to prepare connection URL.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        load_dotenv()
        WEATHER_KEY = os.getenv('WEATHER_KEY')
        WEATHER_LAT = os.getenv('WEATHER_LAT')
        WEATHER_LON = os.getenv('WEATHER_LON')
        if None in (WEATHER_KEY, WEATHER_LAT, WEATHER_LON):
            self.url = None
        else:
            self.url = f'https://api.openweathermap.org/data/2.5/air_pollution?lat={WEATHER_LAT}&lon={WEATHER_LON}&appid={WEATHER_KEY}'
        self.air_data = {}
        self.icons = (u'\uf118', u'\uf118', u'\uf11a', u'\uf119', u'\uf119')

    @view_fallback
    def _epd_change(self, first_call):
        logger.info('%s is running', self.name)
        '''
        IMPORTANT!
        
        Below positions of text and font sizes are chosen arbitrary and they are adjusted to 200x200 EPD, adjust them to your needs!
        Also - units are metrical.
        '''
        if not self.url:
            logger.error('URL not created, serving fallback image!')
            raise ValueError
        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Impact.ttf', 22)
        font_large = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Impact.ttf', 32)
        font_awesome = ImageFont.truetype('/usr/share/fonts/truetype/font-awesome/fontawesome-webfont.ttf', 32)

        aqi = self.air_data.get('aqi')
        if aqi not in range(1,6):
            aqi_label = 'AQI:  N/A'
            aqi = 5
        else:
            aqi_label = f'AQI:  {aqi} / 5'

        _, _, aqi_label_width, aqi_label_height = draw.multiline_textbbox((0,0), aqi_label, font_large)
        
        draw.text((0, 0), aqi_label, font = font_large, fill = 0)
        draw.text((aqi_label_width + 5, 5), self.icons[aqi - 1], font = font_awesome, fill = 0)

        margin_top = aqi_label_height + 5
        column_width = self.epd.width//2

        titles = [f'{key.upper()}: {value}' for key, value in self.air_data.items() if value != None and key != 'aqi']
        wrapped_data = wrap_titles(column_width, self.epd.height, font, titles)

        current_height = margin_top
        current_width = 0

        for data in wrapped_data:
            draw.text((current_width, current_height), data.get('wrapped_title'), font = font, fill = 0)
            current_height += data.get('text_height') + 4
            if current_height > self.epd.height - 30:
                current_height = margin_top
                current_width = column_width

        self.image = image
        self._rotate_image()
        self.epd.display(self.epd.getbuffer(self.image))
        
    def _get_data(self):
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
        except:
            logger.error('Unable to collect the data from OpenWeather API.')
            return {}

    def _conditional(self, *args, **kwargs):
        air_data = self._get_data()
        if not air_data:
            return False
        if bool(kwargs['first_call']) or air_data != self.air_data:
            self.air_data = air_data
            return True
        return False
        
