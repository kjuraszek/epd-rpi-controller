FROM python:3.9-slim-buster
RUN apt-get update && apt-get upgrade -y
RUN apt-get install libpq-dev build-essential -y
WORKDIR /code
RUN mkdir controller
COPY controller controller
COPY Makefile .
COPY epd-rpi-controller.cfg .
RUN make install

CMD ["venv/bin/python3.9", "controller/main.py"]