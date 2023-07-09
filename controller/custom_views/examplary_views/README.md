# Examplary views

A collection of prepared view classes ready to use.
> ⚠️**Warning!** Those classes use additional packages and environment variables - see `views_requirements.txt` and `views_env` files. Update your `.env` and `custom_requirements.txt` files to use those views properly.

Every view must be constructed with two parameters:

- `name` - view instance name
- `interval` - how often view should refresh, `0` if it should be "*static*".

> ⚠️**Warning!** `interval` value must be either `0` or higher than EPD's refresh rate.

If a view angle should be different than set in config it can be overriden by optional `view_angle` parameter.

Some of those views can be seen on this video:

[![EPD RPi Controller](/images/epd-rpi-controller-yt.jpg)](https://youtu.be/IhibN0U2Lx4?t=127 "Raspberry Pi Epaper Display Controller")

> ⚠️**Important!** Some of those Views use third party API's - before use make sure you follow their terms and conditions.

## AirPollutionView

This View displays the data from OpenWeather API `/air_pollution` endpoint.
View uses env vars:

- `WEATHER_KEY` - OpenWeather API key
- `WEATHER_LAT` - longitude
- `WEATHER_LON` - latitude

View uses additional packages:

- `requests`

### AirPollutionView examplary usage

    examplary_views.AirPollutionView(name='Air pollution view', interval=60)

## BaseView

This is a boilerplate for other views - it has got defined `fallback` method but `_epd_change` method must be defined in child class in order to work properly - see `DummyView`.

## BrokenDummyView

A View based on DummyView class, but it raises an Exception so it always serves a fallback image.

### BrokenDummyView examplary usage

    examplary_views.BrokenDummyView(name='Broken Dummy view', interval=0, view_angle=180)

## ChartView

Chart view is a boilerplate for chart views.

Methods `_get_data` and `_draw_plot` must be implemented in child class in order to work properly - see `DummyChartView`.

## ClockView

This View displays a simple clock with current date.

### ClockView examplary usage

    examplary_views.ClockView(name='clock', interval=1)

## ConditionalDummyView

A View based on DummyView class, it displays the image conditionally.

### ConditionalDummyView examplary usage

    examplary_views.ConditionalDummyView(name='Conditional Dummy view', interval=0)

## DummyChartView

View shows dummy basic chart with a random data.

View uses additional packages:

- `matplotlib`

### DummyChartView examplary usages

    examplary_views.DummyChartView(plot_type='stem', figsize=(2, 2), x_label='X LABEL', y_label='Y LABEL', name='DummyChartView', interval=10),
    examplary_views.DummyChartView(figsize=(2, 2), plot_adjustment=(0.19, 0.15, 0.99, 0.95), name='DummyChartView 2', interval=0)

## DummyView

A simple View displaying *Hello World*-like text.

### DummyView examplary usage

    examplary_views.DummyView(name='Dummy view', interval=0)

## ImageView

A View displays an image from certain location - the best idea to store images in rhe `/assets` directory, because it will be copied to a Docker image of Controller.
Parameters passed to a constructor:

- `image_path` - path to a `.jpg` image file

### ImageView examplary usage

    examplary_views.ImageView(name='Image', interval=0, image_path='assets/dog_image.jpg')

## LastFmView

A View displays currently played track from a certain Last.fm account.
View uses env vars:

- `LASTFM_APIKEY` - Last.fm API key
- `LASTFM_USER` - Last.fm user name to show

View uses additional packages:

- `requests`

### LastFmView examplary usage

    examplary_views.LastFmView(name='lastfm', interval=0)

## QRCodeUiView

A View displays QR code with URL to web user interface.
View uses env vars:

- `VITE_UI_PORT` - port on which Controller's UI will be running (already defined in main .env file)
- `VITE_HOSTNAME` - hostname (IP) by which UI will be accessible via browser

View uses additional packages:

- `qrcode`

### QRCodeUiView examplary usage

    examplary_views.QRCodeUiView(name='QRcode UI', interval=0)

## QRCodeWiFiView

A View displays QR code to connect to a WiFi network.
View uses env vars:

- `WIFI_SSID` - network SSID
- `WIFI_PASS` - network password
- `WIFI_TYPE` - network type (eg. WPA2)
- `WIFI_HIDDEN` \[Optional\] - if network is hidden variable must be set to `true`

View uses additional packages:

- `qrcode`

### QRCodeWiFiView examplary usage

    examplary_views.QRCodeWiFiView(name='QRcode WiFi', interval=0)

## QuoteView

A View displays a quote.
Parameters passed to a constructor:

- `quote` - a quote displayed in italic font
- `author` - author of the quote, displayed below

### QuoteView examplary usage

    examplary_views.QuoteView(name='Quote', interval=0, quote='Now, I am become Death, the destroyer of worlds.', author='J. Robert Oppenheimer'),

## RSSView

A View displays a stream of RSS feed.
View uses additional packages:

- `feedparser`

Parameters passed to a constructor:

- `rss_url` - URL of the RSS

### RSSView examplary usage

    examplary_views.RSSView(name='RSS', interval=0, rss_url='https://hnrss.org/newest?count=10')

## SystemInfoView

This view is displaying: CPU temperature, disk usage, CPU utilization, memory usage and swapped memory usage.
View uses additional packages:

- `psutil`

### SystemInfoView examplary usage

    examplary_views.SystemInfoView(name='SystemInfoView', interval=10)

## SpeedTestView

A View triggers SpeedTest and displays the result. It may take some time.
View uses additional packages:

- `speedtest-cli`

### SpeedTestView examplary usage

    examplary_views.SpeedTestView(name='SpeedTest', interval=0)

## SpotifyView

View displays informations about currently played track by user.
View uses env vars (which are defined via Spotify Dashboard):

- `SPOTIPY_CLIENT_ID` - Spotify Client ID
- `SPOTIPY_CLIENT_SECRET` - Spotify Client Secret
- `SPOTIPY_REDIRECT_URI` - Spotify Redirect Uri

View uses additional packages:

- `requests`
- `spotipy`

Before first use application must be authorized, you can use a command `make prepare-spotipy` and follow the instructions in terminal:

- go to URL printed in your console, it starts with `https://accounts.spotify.com/authorize?client_id=`
- paste in the terminal URL  you've been redirected to (eg. `<SPOTIPY_REDIRECT_URI>/?code=...`), even if it ends with connection or similiar error

See more about authorization here: <https://spotipy.readthedocs.io/en/2.22.1/#authorization-code-flow>

### SpotifyView examplary usages

    examplary_views.SpotifyView(name='SpotifyView', interval=360)
    examplary_views.SpotifyView(name='SpotifyView 2', interval=360, album_cover_mode=True)

## TextView

A View displays simple italic text.
Parameters passed to a constructor:

- `text` - text which will be displayed in italic font

### TextView examplary usage

    examplary_views.TextView(name='text', interval=0, text='Lorem ipsum dolor sit amet...')

## WeatherView

This View displays the data from OpenWeather API `/weather` endpoint.
View uses env vars:

- `WEATHER_KEY` - OpenWeather API key
- `WEATHER_LAT` - longitude
- `WEATHER_LON` - latitude

View uses additional packages:

- `requests`

### WeatherView examplary usage

    examplary_views.WeatherView(name='Weather', interval=60)

## WeatherForecastHourlyView

This View displays a hourly temperature forecast as a bar chart based on OpenWeather API `/forecast` endpoint.
View uses env vars:

- `WEATHER_KEY` - OpenWeather API key
- `WEATHER_LAT` - longitude
- `WEATHER_LON` - latitude

View uses additional packages:

- `requests`
- `matplotlib`

### WeatherForecastHourlyView examplary usages

    examplary_views.WeatherForecastHourlyView(name='WeatherForecast', interval=600, figsize=(2, 2), x_label='temperature [°C]', y_label='time [hours]', timestamps=5, hours_additive=True)
    examplary_views.WeatherForecastHourlyView(name='WeatherForecast 2', interval=600, plot_title='Forecast Hourly', plot_adjustment=(0.19, 0.15, 0.99, 0.95))

## WeatherForecastDailyView

This View displays a daily temperature forecast as a bar chart based on OpenWeather API `/forecast` endpoint.
View uses env vars:

- `WEATHER_KEY` - OpenWeather API key
- `WEATHER_LAT` - longitude
- `WEATHER_LON` - latitude

View uses additional packages:

- `requests`
- `matplotlib`

### WeatherForecastDailyView examplary usages

    examplary_views.WeatherForecastDailyView(name='WeatherForecastDaily', interval=600, figsize=(2, 2), x_label='temperature [°C]', y_label='time [days]', max_days=4, mode='max')
    examplary_views.WeatherForecastDailyView(name='WeatherForecastDaily 2', interval=600, figsize=(2, 2), plot_title='Forecast Daily', plot_adjustment=(0.19, 0.15, 0.99, 0.95))
