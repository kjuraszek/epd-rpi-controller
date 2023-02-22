"""
Weather view class
"""

import logging
import os

from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import requests
from requests.adapters import HTTPAdapter, Retry

from custom_views.examplary_views.base_view import BaseView
from src.helpers import view_fallback


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# pylint: disable=R0801
class WeatherView(BaseView):
    '''
    Weather view is displaying current: temperature, pressure, humidity and wind based on the data from OpenWeather API.
    
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
            self.url = f'https://api.openweathermap.org/data/2.5/weather?lat={WEATHER_LAT}&lon={WEATHER_LON}&appid={WEATHER_KEY}&units=metric'
        self.temperature = None
        self.pressure = None
        self.humidity = None
        self.wind = None

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
        font = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Impact.ttf', 70)
        font_small = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Impact.ttf', 36)
        font_awesome = ImageFont.truetype('/usr/share/fonts/truetype/font-awesome/fontawesome-webfont.ttf', 36)
        
        draw.text((0, -10), str(self.temperature) + ' °C', font = font, fill = 0)
        
        draw.line((0, 68, 200, 68), fill = 0, width = 8)
        
        draw.text((0, 78), u'\uf11d', font = font_awesome, fill = 0)
        draw.text((50, 72), str(self.wind) + ' m/s', font = font_small, fill = 0)
        
        draw.text((10, 118), u'\uf043', font = font_awesome, fill = 0)
        draw.text((50, 112), str(self.humidity) + ' %', font = font_small, fill = 0)

        draw.text((4, 158), u'\uf066', font = font_awesome, fill = 0)
        draw.text((50, 152), str(self.pressure) + ' hPa', font = font_small, fill = 0)
        
        self.image = image
        self._rotate_image()
        self.epd.display(self.epd.getbuffer(self.image))
        
    def _get_weather(self):
        try:
            session = requests.Session()
            retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
            session.mount('http://', HTTPAdapter(max_retries=retries))
            session.mount('https://', HTTPAdapter(max_retries=retries))

            data = session.get(self.url).json()
            
            temperature = round(data.get("main", {}).get("temp"))
            pressure = round(data.get("main", {}).get("pressure"))
            humidity = round(data.get("main", {}).get("humidity"))
            wind = round(data.get("wind", {}).get("speed"))
            return (temperature, pressure, humidity, wind)
        except:
            logger.error('Unable to collect the data from OpenWeather API.')
            return (None, None, None, None)

    def _conditional(self, *args, **kwargs):
        temp_temperature, temp_pressure, temp_humidity, temp_wind = self._get_weather()
        if None in (temp_temperature, temp_pressure, temp_humidity, temp_wind):
            return False
        if bool(kwargs['first_call']) or (temp_temperature, temp_pressure, temp_humidity, temp_wind) != (self.temperature, self.pressure, self.humidity, self.wind):
            self.temperature = temp_temperature
            self.pressure = temp_pressure
            self.humidity = temp_humidity
            self.wind = temp_wind
            return True
        return False
        
