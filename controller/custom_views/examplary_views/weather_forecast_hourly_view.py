"""
Weather forecast hourly view class
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
from matplotlib import ticker, pyplot

from custom_views.examplary_views.base_view import BaseView
from src.helpers import view_fallback


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# pylint: disable=R0801
class WeatherForecastHourlyView(BaseView):
    '''
    Weather forecast view is displaying daily temperature forecast based on the data from OpenWeather API.

    It uses environment variables to prepare connection URL.
    '''
    def __init__(self, *, timestamps: int = 6, hours_additive: bool = False, show_labels: bool = True, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        load_dotenv()

        weather_key = os.getenv('WEATHER_KEY')
        weather_lat = os.getenv('WEATHER_LAT')
        weather_lon = os.getenv('WEATHER_LON')

        if None in (weather_key, weather_lat, weather_lon):
            self.url = None
        else:
            self.url = f'https://api.openweathermap.org/data/2.5/forecast?lat={weather_lat}&lon={weather_lon}'\
                       f'&appid={weather_key}&units=metric&cnt={timestamps}&cnt={timestamps}'
        self.forecast = None
        self.timestamps = timestamps
        self.hours_additive = hours_additive
        self.show_labels = show_labels

    @view_fallback
    def _epd_change(self, first_call: bool) -> None:
        logger.info('%s is running', self.name)
        if not self.url:
            logger.error('URL not created, serving fallback image!')
            raise ValueError
        if self.timestamps not in range(1, 41):
            logger.error('Wrong timestamps range, serving fallback image!')
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
        processed_data = {}
        for index, element in enumerate(data.get('list', [])):
            temperature = int(element.get('main').get('temp'))
            timestamp = datetime.datetime.fromtimestamp(element.get('dt'))
            if self.hours_additive:
                if index == 0:
                    hour = f'{timestamp.hour}:'
                else:
                    hour = f'+{index * 3}'
            else:
                hour = f'{timestamp.hour}:{"." * (index//8)}'

            processed_data[hour] = temperature

        return processed_data

    def _draw_plot(self):
        '''
        IMPORTANT!

        Below positions, margins etc. are chosen arbitrary and they are adjusted to 200x200 EPD, adjust them to your needs!
        Also - units are metrical.
        '''

        hours = list(self.forecast.keys())
        values = list(self.forecast.values())
        margin = 2
        figsize = (2, 2)
        x_label = 'time [hours]'
        y_label = 'temperature [°C]'

        plot_adjustment = (0.29, 0.25, 0.99, 0.95) if self.show_labels else (0.19, 0.15, 0.99, 0.95)

        heights = [margin + value - min(values) for value in values]
        fig = pyplot.figure(figsize=figsize).gca()
        fig.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        if self.show_labels:
            fig.set_ylabel(y_label)
            fig.set_xlabel(x_label)

        pyplot.bar(hours, heights, bottom=min(values) - margin, color='black')
        pyplot.ylim(bottom=min(values) - margin, top=max(values) + margin)
        pyplot.subplots_adjust(*plot_adjustment)

        buffer = io.BytesIO()
        pyplot.savefig(buffer, format='png')
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
