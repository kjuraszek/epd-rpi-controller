FROM python:3.9-slim-buster
ARG TIMEZONE
ARG VITE_API_PORT
RUN apt-get update && apt-get upgrade -y
RUN apt-get install libpq-dev build-essential -y
RUN echo "deb http://httpredir.debian.org/debian buster main contrib non-free" > /etc/apt/sources.list \
    && echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections \
    && apt-get update \
    && apt-get install -y ttf-mscorefonts-installer fonts-font-awesome
RUN cp "/usr/share/zoneinfo/${TIMEZONE}" /etc/localtime || true
RUN echo "${TIMEZONE}" >  /etc/timezone
WORKDIR /code
RUN mkdir controller
COPY controller controller
COPY Makefile .
COPY epd-rpi-controller.cfg .
COPY .env .
RUN make install

EXPOSE $VITE_API_PORT

ENV EPD_RPI_DOCKERIZED true

CMD ["venv/bin/python3.9", "controller/main.py"]