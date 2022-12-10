# EPD Rpi Controller

Waveshare epaper display controller for Raspberry Pi. Project is mostly written in Python 3.9 and is based on Waveshare EPD library, Apache Kafka and Docker containers.

## About the project

This project simplifies displaying custom informations on Epaper display connected to a Raspberry Pi. Display part is realized by a `View` - configured object with a defined method `show` which performs directly on EPD object. Views are managed by a `View Manager` - they can be switched automatically by some time interval and in a different order. EPD can be simulated using config option - an image with a current view will be generated (instead of displaying it on a physical device).
In addition controller also allows to switch between `Views` using physical buttons.

## Prerequisites

- Raspberry Pi (tested using Rpi 3B, v4 should also be fine) with 2GB memory ()
- supported Linux operating system installed (eg. Ubuntu Server)
- Docker and Docker Compose installed
- GNU Make
- EPD display supported by Waveshare EPD library
- `[Optional]` Postman or other application/script to send `POST` requests and invoke EPD changes
- `[Optional]` physical buttons

## Running the project

Below are instructions on running this project.

### Create .cfg file

Create `epd-rpi-controller.cfg` (copy epd-rpi-controller.example.cfg file) and make adjustments

### Prepare Python venv

Create and set Python virtual environment

### Install Python dependencies

Install Python dependencies from requirements.txt

### Create docker network

Create docker network `epd-rpi-network`

### Run docker compose

Run docker compose to run Kafka - Zookeeper, Kafka Server and Kafka REST-api

### Run controller

Run controller/main.py
