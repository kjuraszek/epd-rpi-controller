"""
Weather forecast daily view class
"""

import io
import datetime
import os
from typing import Any, Optional

from dotenv import load_dotenv
import requests
from requests.adapters import HTTPAdapter, Retry
from matplotlib import ticker, pyplot

from custom_views.examplary_views.chart_view import ChartView
from logger import logger


# pylint: disable=R0801
class WeatherForecastDailyView(ChartView):
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
        self.forecast: dict[str, int] = {}
        self.max_days = max_days
        self.mode = mode

    def _get_data(self) -> Optional[dict[str, int]]:
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

    def _process_data(self, data: dict[Any, Any]) -> dict[str, int]:
        day_to_temps: dict[str, list[int]] = {}
        processed_data: dict[str, int] = {}
        for element in data.get('list', []):

            temperature = int(element.get('main').get('temp'))
            timestamp = datetime.datetime.fromtimestamp(element.get('dt'))
            day = f'{timestamp.day}.'

            if day not in day_to_temps:
                if len(day_to_temps) == self.max_days:
                    break
                day_to_temps[day] = []
            day_to_temps[day].append(temperature)

        for day, temps in day_to_temps.items():
            if self.mode == 'avg':
                processed_data[day] = int(sum(temps)/len(temps))
            elif self.mode == 'max':
                processed_data[day] = int(max(temps))

        return processed_data

    def _draw_plot(self) -> io.BytesIO:
        '''
        IMPORTANT!

        Below positions, adjustments, margins etc. are chosen arbitrary and they are adjusted to 200x200 EPD, adjust them to your needs!
        Also - units are metrical.
        '''

        y_values = list(self.data.keys())
        x_values = list(self.data.values())
        margin = 2

        heights = [margin + value - min(x_values) for value in x_values]
        fig = pyplot.figure(figsize=self.figsize).gca()
        fig.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        if not None in (self.x_label, self.y_label):
            fig.set_ylabel(self.y_label)
            fig.set_xlabel(self.x_label)

        pyplot.bar(y_values, heights, bottom=min(x_values) - margin, color='black')
        pyplot.ylim(bottom=min(x_values) - margin, top=max(x_values) + margin)
        if self.plot_adjustment:
            pyplot.subplots_adjust(*self.plot_adjustment)

        buffer = io.BytesIO()
        pyplot.savefig(buffer, format='png')
        return buffer
