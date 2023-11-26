"""
Weather forecast hourly view class
"""

import io
import datetime
import os
from typing import Any, Optional

from dotenv import load_dotenv
import requests
from requests.adapters import HTTPAdapter, Retry
from matplotlib import ticker, pyplot

from logger import logger
from custom_views.examplary_views.chart_view import ChartView


# pylint: disable=R0801
class WeatherForecastHourlyView(ChartView):
    """
    Weather forecast view is displaying daily temperature forecast based on the data from OpenWeather API.

    It uses environment variables to prepare connection URL.
    """

    def __init__(
        self, *, timestamps: int = 6, hours_additive: bool = False, **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        load_dotenv()

        weather_key = os.getenv("WEATHER_KEY")
        weather_lat = os.getenv("WEATHER_LAT")
        weather_lon = os.getenv("WEATHER_LON")

        if None in (weather_key, weather_lat, weather_lon):
            self.url = None
        else:
            self.url = (
                f"https://api.openweathermap.org/data/2.5/forecast?lat={weather_lat}&lon={weather_lon}"
                f"&appid={weather_key}&units=metric&cnt={timestamps}&cnt={timestamps}"
            )
        self.timestamps = timestamps
        self.hours_additive = hours_additive

    def _get_data(self) -> Optional[dict[str, int]]:
        try:
            session = requests.Session()
            retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
            session.mount("http://", HTTPAdapter(max_retries=retries))
            session.mount("https://", HTTPAdapter(max_retries=retries))

            data = session.get(self.url).json()  # type: ignore
            forecast = self._process_data(data)
            return forecast
        except Exception:  # pylint: disable=W0703
            logger.error("Unable to collect the data from OpenWeather API.")
            return None

    def _process_data(self, data: dict[Any, Any]) -> dict[str, int]:
        """Method processes gathered data"""

        processed_data = {}
        for index, element in enumerate(data.get("list", [])):
            temperature = int(element.get("main").get("temp"))
            timestamp = datetime.datetime.fromtimestamp(element.get("dt"))
            if self.hours_additive:
                if index == 0:
                    hour = f"{timestamp.hour}:"
                else:
                    hour = f"+{index * 3}"
            else:
                hour = f'{timestamp.hour}:{"." * (index//8)}'

            processed_data[hour] = temperature

        return processed_data

    def _draw_plot(self) -> io.BytesIO:
        """Method draws a plot basing on the data and returns it as a bytes."""

        y_values = list(self.data.keys())
        x_values = list(self.data.values())
        margin = 2

        heights = [margin + value - min(x_values) for value in x_values]
        fig = pyplot.figure(figsize=self.figsize).gca()
        fig.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        if None not in (self.x_label, self.y_label):
            fig.set_ylabel(self.y_label)
            fig.set_xlabel(self.x_label)

        pyplot.bar(y_values, heights, bottom=min(x_values) - margin, color="black")
        pyplot.ylim(bottom=min(x_values) - margin, top=max(x_values) + margin)
        if self.plot_adjustment:
            pyplot.subplots_adjust(*self.plot_adjustment)

        if self.plot_title:
            pyplot.title(self.plot_title)
        buffer = io.BytesIO()
        pyplot.savefig(buffer, format="png")
        pyplot.close()
        return buffer

    def _conditional(self, *args: Any, **kwargs: Any) -> bool:
        data = self._get_data()
        if not data:
            return False
        if bool(kwargs["first_call"]) or (data != self.data):
            self.data = data
            return True
        return False
