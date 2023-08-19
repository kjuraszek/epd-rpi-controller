# EPD Rpi Controller

Epaper display controller for Raspberry Pi. Project is mostly written in Python 3.9, web interface in Vue.js 3. It is based on Waveshare EPD library, Apache Kafka and Docker containers.

## About the project

[![EPD RPi Controller](/images/epd-rpi-controller-yt.jpg)](https://www.youtube.com/watch?v=IhibN0U2Lx4 "Raspberry Pi Epaper Display Controller")

This project simplifies displaying custom informations on Epaper display connected to a Raspberry Pi. Display part is realized by a `View` - configured object with a defined method `_epd_change` which performs directly on EPD object. Views are managed by a `View Manager` - they can be switched automatically by some time interval and in a different order. EPD can be simulated using config option - an image with a current view will be generated (instead of displaying it on a physical device). Controller exposes an API to trigger view changes via specific `GET` request. Web user interface is also created to make switching views even simplier.

In addition controller also allows to switch between `Views` using physical buttons.
More about Controller: go to [Controller](/controller/README.md).

### Examplary views

Some examples of predefined views classes.

### Clock

![ClockView](/controller/custom_views/examplary_views/images/ClockView.jpg)

### Image

![ImageView](/controller/custom_views/examplary_views/images/ImageView.jpg)

### QRCode WiFi

![QRCodeWiFiView](/controller/custom_views/examplary_views/images/QRCodeWiFiView.jpg)

### System Info

![SystemInfoView](/controller/custom_views/examplary_views/images/SystemInfoView.jpg)

### SpeedTest

![SpeedTestView](/controller/custom_views/examplary_views/images/SpeedTestView.jpg)

### Spotify

![SpotifyView](/controller/custom_views/examplary_views/images/SpotifyView.jpg)

### Weather

![WeatherView](/controller/custom_views/examplary_views/images/WeatherView.jpg)

### Weather Forecast

![WeatherForecastDailyView](/controller/custom_views/examplary_views/images/WeatherForecastDailyView.jpg)

... and more, see [Examplary Views](/controller/custom_views/examplary_views/README.md).

## Prerequisites

- Raspberry Pi (tested using Rpi 3B, v4 should also be fine) with 2GB memory (if less than 2GB - swapping memory *might* do the trick, see `dphys-swapfile`)
- supported Linux operating system installed (eg. Ubuntu Server)
- Docker and Docker Compose installed
- GNU Make
- EPD display supported by Waveshare EPD library
- `[Optional]` Postman or other application/script to send `POST` requests and invoke EPD changes (using Kafka REST)
- `[Optional]` physical buttons
- `[Optional]` msttcorefonts and font-awesome fonts installed (used in examplary views - needed only for local development, containers will include those fonts)

## Running the project

Below are instructions on running this project. For a long term deployment ("production") it is recommended to run both the Controller and UI in Docker containers. In other hand running them locally will suit better for testing.

> ⚠️**Important!** All below `make` commands are adjusted to run from project's root (and **not** from `/controller`, `/front` etc.).

### Prepare environment

Run the command:

`make prepare`

which:

- creates `epd-rpi-controller.cfg` (copies epd-rpi-controller.example.cfg file)
- creates `.env` (copies .env.example file)
- creates empty `assets` dir which should store all assets used by Controller (images etc.)
- prepares Python virtual environment
- installs Python dependencies
- installs JS dependencies
- creates docker network `epd-rpi-network`

You should adjust config and .env files to your needs - however bear in mind that all defined variables/parameters in examplary .cfg/.env files are crucial for controller to work properly. Also to run the Controller you must prepare Views in `controller/custom_views/views.py` (file by default doesn't exist) - take a look on file `controller/custom_views/example.py`.
Alternatively you can use a command:

`make create-views-file`

to copy contents from `example.py`.

Also custom requirements.txt file is supported.
To learn more about custom views and custom_requirements.txt go to [Custom views](/controller/custom_views/README.md)
There are also some predefined View classes - see [Examplary Views](/controller/custom_views/examplary_views/README.md).

### Prepare Kafka stack

Run Kafka stack in Docker containers - Zookeeper and Kafka Server

`make run-docker`

or

`make run-docker-kafka-full` to run with Kafka REST API and Kafdrop

> ⚠️**Warning!** Kafka stack (Zookeper, Kafka) is crucial component of this project - if one of its the containers is not working or exiting prematurely you should examine the reason for such behaviour before moving forward. `Kafka REST` and `Kafdrop` are optional services.

- Zookeeper will be running at port `2181`
- Kafka will be running at port `9092` and will listen on port  `29092` for a REST API
- Kafka REST API will be available at [localhost:8082](http://localhost:8082/)
- Kafka UI will be available at [localhost:19000](http://localhost:19000/)

### Running the controller

Controller can be executed directly via Python or in a Docker container. The former is suggested when creating and adjusting views (especially with MockedEPD) whilst the latter - rather on "production", when everything works (due to eg. building Docker image which is time-consuming).
Controller will expose an API on selected port from `.env` (by default [localhost:8888/api/](http://localhost:8888/api/) ).
Also Swagger documentation will be available, under [localhost:8888/api/doc/](http://localhost:8888/api/doc/) .

#### Executing via Python

Firstly make sure Kafka stack is up and running, if not run:

`make run-docker`

and then run the controller using a command:

`make run-controller`

#### Controller in a container

Run the controller with Kafka stack using a command

`make run-docker-ctrl`

> When making changes in the code make sure you're using the newest image - remember to run `make build-docker` before running run-docker command.

### Running the UI \[OPTIONAL\]

A simple user interface is built with Vue.js 3 and Vuetify. For now it displays current view (as image) and allows to switch between views.

Firstly make sure the controller is up and running - either in container or locally.
UI will run on selected port from `.env` (by default [localhost:3000](http://localhost:3000/) ).

#### Running UI locally

Run the UI using a command:

`make run-ui`

#### UI in a container

Run the UI with Kafka stack using a command

`make run-docker-ctrl-ui` to run UI with a Controller in containers

or

`make run-docker-ui` to run UI in a container (Controller should be started in a new terminal with command `make run-controller`)

> When making changes in the code make sure you're using the newest image - remember to run `make build-docker` before running run-docker command.

Alternatively you can run the controller with web UI, Kafka REST API and Kafka's web UI - Kafdrop via command:

`make run-docker-all`

and then:

- Controller and UI will run on selected ports from `.env` (by default [localhost:8888](http://localhost:8888/) and [localhost:3000](http://localhost:3000/) respectively)
- Kafka REST API will be available at [localhost:8082](http://localhost:8082/)
- Kafka UI will be available at [localhost:19000](http://localhost:19000/).

## Configuration file

Config is stored in a file `epd-rpi-controller.cfg` (file by default doesn't exist).

### `main` section

| Option | Purpose | Values |
| --- | --- | --- |
| producer_interval | Interval (in seconds) | positive integers or 0 - 0 means no interval |
| producer_asc_order | Order of switching views, `yes` means ascending. Works only if `producer_interval` is set. | bool (yes/no) |
| starting_view | Index of View which will be the starting one | positive integers or 0 - 0 means no interval |
| epd_model | EPD model which will be importen from Waveshare library | model name or `mock` |
| mocked_epd_width | Width of mocked EPD display (only used when `epd_model=mock`) | positive integer |
| mocked_epd_height | Height of mocked EPD display (only used when `epd_model=mock`) | positive integer |
| clear_epd_on_exit | Clears display on exit when setted | bool (yes/no) |
| view_angle | An angle by which the display will be rotated | integer |
| use_buttons | Enables support for two physical buttons (left and right) | bool (yes/no) |
| left_button_pin | GPIO number (not physical pin on board!) of pin connected to the left button | positive integer |
| right_button_pin | GPIO number (not physical pin on board!) of pin connected to the right button | positive integer |

### `kafka` section

| Option | Purpose | Values |
| --- | --- | --- |
| view_manager_topic | Name of the *topic* used by Kafka | string compatible with Kafka topic naming rules |
| logging_level | logging level for kafka | level name eg. `DEBUG`, `INFO` etc. |

### `matplotlib` section

| Option | Purpose | Values |
| --- | --- | --- |
| logging_level | logging level for matplotlib | level name eg. `DEBUG`, `INFO` etc. |

### `tornado` section

| Option | Purpose | Values |
| --- | --- | --- |
| logging_level | logging level for tornado | level name eg. `DEBUG`, `INFO` etc. |

### other sections

Sections below a comment: `; logging config` are related to a main logger, see: <https://docs.python.org/3/library/logging.config.html#configuration-file-format>

## .env file

Variables defined in .env file (file by default doesn't exist):

| Variable | Purpose | Values |
| --- | --- | --- |
| TIMEZONE | Timezone used in Controller container | valid timezone eg. `Europe/Paris`, `UTC` etc. |
| VITE_API_PORT | Port on which Controller's API will be running (added `VITE_` prefix to allow import in Vue.js) | positive integer |
| VITE_UI_PORT | Port on which Controller's UI will be running | positive integer |
| EPD_RPI_CONFIG_FILE | File with configuration, optional variable - by default `epd-rpi-controller.cfg` | string |

## Using mocked EPD

To test how Views will look you can use a Mocked EPD first - each View content will be saved to a file `mocked_epd.png`. To turn on this mode edit config:

- set `epd_model=mock`
- set desired width and height (`mocked_epd_width` and `mocked_epd_height`)

## Using physical buttons

EPD Rpi Controller also supports usage of two physical buttons - one button for triggering *previous* view and the other one - to trigger the *next* view. Both GPIOs are in BCM mode - **GPIO number is used, instead of physical pin number on the board**. GPIOs are connected to internal *PULL_UP* resistor and are working in *INPUT* mode.
Both buttons are connected to:

- GND
- with a 330 Ω (ohm) resistor (for Rpi safety) to a corresponding GPIO

To use buttons edit config file and set `use_buttons = yes`. Also set `left_button_pin` and `right_button_pin` to desired **GPIO** numbers.

![Electric Circuit for EPD Rpi Controller](/images/electric_circuit.png)
*Electric Circuit for EPD Rpi Controller with connected buttons*

Examplary button config for a circuit above would be:

    use_buttons = yes
    left_button_pin = 26
    right_button_pin = 16
