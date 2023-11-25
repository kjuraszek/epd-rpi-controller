"""
Examples with classes from examplary_views
"""


from custom_views import examplary_views

VIEWS = [
    examplary_views.AirPollutionView(name="AirPollutionView", interval=60),
    examplary_views.BrokenDummyView(name="BrokenDummyView", interval=0, view_angle=180),
    examplary_views.ClockView(name="ClockView", interval=1),
    examplary_views.ConditionalDummyView(name="ConditionalDummyView", interval=0),
    examplary_views.DummyChartView(
        plot_type="stem",
        figsize=(2, 2),
        x_label="X LABEL",
        y_label="Y LABEL",
        name="DummyChartView",
        interval=10,
    ),
    examplary_views.DummyChartView(
        figsize=(2, 2),
        plot_adjustment=(0.19, 0.15, 0.99, 0.95),
        name="DummyChartView 2",
        interval=0,
    ),
    examplary_views.DummyView(name="DummyView", interval=0),
    examplary_views.ImageView(
        name="ImageView", interval=0, image_path="assets/dog_image.jpg"
    ),
    examplary_views.LastFmView(name="LastFmView", interval=0),
    examplary_views.QRCodeUiView(name="QRCodeUiView", interval=0),
    examplary_views.QRCodeWiFiView(name="QRCodeWiFiView", interval=0),
    examplary_views.QuoteView(
        name="QuoteView",
        interval=0,
        quote="Now, I am become Death, the destroyer of worlds.",
        author="J. Robert Oppenheimer",
    ),
    examplary_views.RSSView(
        name="RSSView", interval=0, rss_url="https://hnrss.org/newest?count=10"
    ),
    examplary_views.SystemInfoView(name="SystemInfoView", interval=10),
    examplary_views.SpeedTestView(name="SpeedTestView", interval=0),
    examplary_views.SpotifyView(name="SpotifyView", interval=360),
    examplary_views.SpotifyView(
        name="SpotifyView 2", interval=360, album_cover_mode=True
    ),
    examplary_views.TextView(
        name="TextView", interval=0, text="Lorem ipsum dolor sit amet..."
    ),
    examplary_views.WeatherView(name="WeatherView", interval=60),
    examplary_views.WeatherForecastHourlyView(
        name="WeatherForecastHourlyView",
        interval=600,
        figsize=(2, 2),
        x_label="temperature [°C]",
        y_label="time [hours]",
        timestamps=5,
        hours_additive=True,
    ),
    examplary_views.WeatherForecastHourlyView(
        name="WeatherForecastHourlyView 2",
        interval=600,
        plot_title="Forecast Hourly",
        plot_adjustment=(0.19, 0.15, 0.99, 0.95),
    ),
    examplary_views.WeatherForecastDailyView(
        name="WeatherForecastDaily",
        interval=600,
        figsize=(2, 2),
        x_label="temperature [°C]",
        y_label="time [days]",
        max_days=4,
        mode="max",
    ),
    examplary_views.WeatherForecastDailyView(
        name="WeatherForecastDaily 2",
        interval=600,
        figsize=(2, 2),
        plot_title="Forecast Daily",
        plot_adjustment=(0.19, 0.15, 0.99, 0.95),
    ),
    examplary_views.WeatherForecastHourlyView(
        name="WeatherForecastHourlyView",
        interval=600,
        figsize=(2, 2),
        x_label="time [hours]",
        y_label="temperature [°C]",
        plot_adjustment=(0.29, 0.25, 0.99, 0.95),
        timestamps=5,
        hours_additive=True,
    ),
    examplary_views.WeatherForecastHourlyView(
        name="WeatherForecastHourlyView 2",
        interval=600,
        figsize=(2.25, 2.25),
        plot_title="Forecast Hourly",
        plot_adjustment=(0.19, 0.1, 0.99, 0.9),
    ),
    examplary_views.WeatherForecastDailyView(
        name="WeatherForecastDaily",
        interval=600,
        figsize=(2, 2),
        x_label="time [days]",
        y_label="temperature [°C]",
        plot_adjustment=(0.29, 0.25, 0.99, 0.95),
        max_days=4,
        mode="max",
    ),
    examplary_views.WeatherForecastDailyView(
        name="WeatherForecastDaily 2",
        interval=600,
        figsize=(1.8, 1.8),
        plot_adjustment=(0.19, 0.15, 0.99, 0.95),
    ),
]
