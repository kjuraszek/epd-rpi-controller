FROM python:3.9-slim-buster
RUN apt-get update && apt-get upgrade -y
RUN apt-get install libpq-dev build-essential -y
RUN echo "deb http://httpredir.debian.org/debian buster main contrib non-free" > /etc/apt/sources.list \
    && echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections \
    && apt-get update \
    && apt-get install -y ttf-mscorefonts-installer fonts-font-awesome
WORKDIR /code
RUN mkdir controller
COPY controller controller
COPY Makefile .
COPY epd-rpi-controller.cfg .
RUN make install

EXPOSE 8888

ENV EPD_RPI_DOCKERIZED true

CMD ["venv/bin/python3.9", "controller/main.py"]