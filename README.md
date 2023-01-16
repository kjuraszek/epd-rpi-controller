# EPD Rpi Controller

Waveshare epaper display controller for Raspberry Pi. Project is mostly written in Python 3.9 and is based on Waveshare EPD library, Apache Kafka and Docker containers.

## About the project

![EPD RPi Controller](/images/epd-rpi-controller.jpg)

This project simplifies displaying custom informations on Epaper display connected to a Raspberry Pi. Display part is realized by a `View` - configured object with a defined method `show` which performs directly on EPD object. Views are managed by a `View Manager` - they can be switched automatically by some time interval and in a different order. EPD can be simulated using config option - an image with a current view will be generated (instead of displaying it on a physical device).
In addition controller also allows to switch between `Views` using physical buttons.

## Prerequisites

- Raspberry Pi (tested using Rpi 3B, v4 should also be fine) with 2GB memory (if less than 2GB - swapping memory *might* do the trick, see `dphys-swapfile`)
- supported Linux operating system installed (eg. Ubuntu Server)
- Docker and Docker Compose installed
- GNU Make
- EPD display supported by Waveshare EPD library
- `[Optional]` Postman or other application/script to send `POST` requests and invoke EPD changes
- `[Optional]` physical buttons

## Running the project

Below are instructions on running this project.

### Prepare environment

Run the command:

`make prepare`

which:

- creates `epd-rpi-controller.cfg` (copies epd-rpi-controller.example.cfg file)
- creates `.env` (copies .env.example file)
- prepares Python virtual environment
- installs Python dependencies
- creates docker network `epd-rpi-network`

You should adjust config file to your needs. Also to run the Controller you must prepare Views in `controller/custom_views/views.py` (file by default doesn't exist) - take a look on file `example.py`.
Alternatively you can use a command:

`make create-views-file`

to copy contents from `example.py`.

Also custom requirements.txt file is supported.
To learn more about custom views and requirements go to [Custom views](/controller/custom_views/Readme.md)

### Prepare Kafka stack

Run Kafka stack in Docker containers - Zookeeper, Kafka Server and Kafka REST-api

`make run-docker`

> ⚠️**Warning!** Kafka stack (Zookeper, Kafka, Kafka-REST) is crucial component of this project - if one of its the containers is not working or exiting prematurely you should examine the reason for such behaviour before moving forward.

### Running the controller

Controller can be executed directly via Python or in a Docker container. The former is suggested when creating and adjusting views (especially with MockedEPD) whilst the latter - rather on 'production', when everything works (due to eg. building Docker image which is time-consuming).

#### Executing via Python

Firstly make sure Kafka stack is up and running, if not run:

`make run-docker`

and then run the controller using a command:

`make run-controller`

#### Controller in a container

Run the controller with Kafka stack using a command

`make run-docker-ctrl`

> When making changes in the code make sure you're using the newest image - remember to run `make build-docker` before running run-docker command.

Alternatively you can run Kafka's web UI - Kafdrop via command:

`make run-docker-all`

which will be available at [localhost:19000](http://localhost:19000/).

## Configuration file

Config is stored in a file `epd-rpi-controller.cfg` (file by default doesn't exist).

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
| view_manager_topic | Name of the *topic* used by Kafka | string compatible with Kafka topic naming rules |

## .env file

Variables defined in .env file (file by default doesn't exist):

| Variable | Purpose | Values |
| --- | --- | --- |
| TIMEZONE | Timezone used in Controller container | valid timezone eg. `Europe/Paris`, `UTC` etc. |
| VITE_API_PORT | Port on which Controller's API will be running (added `VITE_` prefix to allow import in Vue.js) | positive integer |
| VITE_UI_PORT | Port on which Controller's UI will be running | positive integer |

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
