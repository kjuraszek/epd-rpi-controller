"""
Weather forecast daily view class
"""

import io
import datetime
import logging
import os
from typing import Any

from dotenv import load_dotenv
from PIL import Image
import requests
from requests.adapters import HTTPAdapter, Retry
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from custom_views.examplary_views.base_view import BaseView
from src.helpers import view_fallback


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# pylint: disable=R0801
class WeatherForecastDailyView(BaseView):
    '''
    Weather forecast view is displaying daily temperature forecast based on the data from OpenWeather API.

    It uses environment variables to prepare connection URL.
    '''
    def __init__(self, *, max_days: int = 6, mode: str = 'avg', **kwargs: Any) -> None:
        super().__init__(**kwargs)
        load_dotenv()

        weather_key = os.getenv('WEATHER_KEY')
        weather_lat = os.getenv('WEATHER_LAT')
        weather_lon = os.getenv('WEATHER_LON')
        if None in (weather_key, weather_lat, weather_lon):
            self.url = None
        else:
            self.url = f'https://api.openweathermap.org/data/2.5/forecast?lat={weather_lat}&lon={weather_lon}'\
                       f'&appid={weather_key}&units=metric'
        self.forecast = None
        self.max_days = max_days
        self.mode = mode

    @view_fallback
    def _epd_change(self, first_call: bool) -> None:
        logger.info('%s is running', self.name)
        if not self.url:
            logger.error('URL not created, serving fallback image!')
            raise ValueError
        if self.max_days not in range(1, 7):
            logger.error('Wrong day range, serving fallback image!')
            raise ValueError

        plot = self._draw_plot()

        image = Image.open(plot)
        if image.size != (self.epd.width, self.epd.height):
            image = image.resize((self.epd.width, self.epd.height))
        image = image.convert('1')

        self.image = image
        self._rotate_image()
        self.epd.display(self.epd.getbuffer(self.image))

    def _get_forecast(self) -> dict[Any]:
        try:
            session = requests.Session()
            retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
            session.mount('http://', HTTPAdapter(max_retries=retries))
            session.mount('https://', HTTPAdapter(max_retries=retries))

            data = session.get(self.url).json()  # type: ignore
            forecast = self._process_data(data)
            return forecast
        except Exception:  # pylint: disable=W0703
            logger.error('Unable to collect the data from OpenWeather API.')
            return None

    def _process_data(self, data):
        day_to_temps = {}
        processed_data = {}
        for el in data.get('list', []):

            temperature = int(el.get('main').get('temp'))
            timestamp = datetime.datetime.fromtimestamp(el.get('dt'))
            day = f'{timestamp.day}.'
            
            if day not in day_to_temps.keys():
                if len(day_to_temps.keys()) == self.max_days:
                    break
                day_to_temps[day] = []
            day_to_temps[day].append(temperature)

        for day, temps in day_to_temps.items():
            if self.mode == 'avg':
                processed_data[day] = int(sum(temps)/len(temps))
            elif self.mode == 'max':
                processed_data[day] = int(max(temps))

        return processed_data

    def _draw_plot(self):
        '''
        IMPORTANT!

        Below positions, margins etc. are chosen arbitrary and they are adjusted to 200x200 EPD, adjust them to your needs!
        Also - units are metrical.
        '''

        days = list(self.forecast.keys())
        values = list(self.forecast.values())
        margin = 2
        figsize = (2, 2)
        x_label = 'time [days]'
        y_label = 'temperature [°C]'

        heights = [margin + value - min(values) for value in values]
        fig = plt.figure(figsize=figsize).gca()
        fig.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        fig.set_ylabel(y_label)
        fig.set_xlabel(x_label)

        plt.bar(days, heights, bottom=min(values) - margin, color='black')
        plt.ylim(bottom=min(values) - margin, top=max(values) + margin)
        plt.subplots_adjust(top=0.95,right=0.99,bottom=0.25,left=0.29)

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        return buffer

    def _conditional(self, *args: Any, **kwargs: Any) -> bool:
        forecast = self._get_forecast()
        if not forecast:
            return False
        if bool(kwargs['first_call']) or (
                forecast != self.forecast):
            self.forecast = forecast
            return True
        return False
