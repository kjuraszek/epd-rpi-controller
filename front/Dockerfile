FROM node:lts-alpine as base

RUN apk update && apk upgrade
WORKDIR /app
RUN mkdir front
COPY front/package.json front/package-lock.json /app/front/
RUN npm --prefix front install

FROM base as build
ARG VITE_API_PORT
ARG VITE_UI_PORT
ENV VITE_API_PORT=$VITE_API_PORT
ENV VITE_UI_PORT=$VITE_UI_PORT
WORKDIR /app

COPY front front
RUN npm run --prefix front build

FROM node:lts-alpine  as final
ARG VITE_API_PORT
ARG VITE_UI_PORT
ENV VITE_API_PORT=$VITE_API_PORT
ENV VITE_UI_PORT=$VITE_UI_PORT

RUN apk update && apk upgrade
RUN npm install -g http-server

WORKDIR /app

RUN mkdir front
COPY --from=build /app/front/dist /app/front/dist

EXPOSE $VITE_UI_PORT

CMD http-server front/dist -p $VITE_UI_PORT
