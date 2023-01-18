FROM node:lts-alpine
ARG VITE_API_PORT
ARG VITE_UI_PORT
ENV VITE_API_PORT=$VITE_API_PORT
ENV VITE_UI_PORT=$VITE_UI_PORT
RUN apk update && apk upgrade
RUN npm install -g http-server
WORKDIR /app
RUN mkdir front
COPY front front
COPY Makefile .
COPY epd-rpi-controller.cfg .
COPY .env .
RUN npm --prefix front install
RUN npm run --prefix front build

EXPOSE $VITE_UI_PORT

CMD http-server front/dist -p $VITE_UI_PORT
