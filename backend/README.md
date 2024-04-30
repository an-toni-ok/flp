# Backend <!-- omit in toc -->

This directory contains the backend part of the flp web application.
It consists of a Flask web application, a Celery instance for running background tasks and a Redis Server, which is working as a message broker between Flask and Celery.

## Contents <!-- omit in toc -->

- [Setup](#setup)
- [Start server](#start-server)
  - [Update the server code](#update-the-server-code)
- [Documentation](#documentation)

## Setup

The easiest way to setup the backend is by using docker compose. If you do not have docker installed, you can follow the [official installation instructions](https://docs.docker.com/get-docker/).
You also need to install docker compose, to do so you can follow the [official installation instructions](https://docs.docker.com/compose/install/).

## Start server

To start the backend applications for the production server, simply execute the following command in this directory and wait a few seconds.

```bash
docker compose up
```

The executed command now automatically starts the containers for Flask, Celery in Redis in the correct sequence. As soon as the start of the containers is completed will you be able to access the Flask web application at http://localhost:5000 (and at http://172.0.0.1:5000) and the Redis Insights at http://localhost:8001 (and at http://172.0.0.1:8001).

### Update the server code

To update the code used in the production server (either the Flask code or the Celery Tasks), a new docker image needs to be generated and used by docker compose. 

Simply execute the following command if the code has changed:

```bash
docker compose up --build
```

## Documentation

The documentation of the API endpoints can be found in the file [openapi.yaml](./openapi.yaml). It serves as a formal declaration of the endpoints and can also be used to test the endpoints.

Further documentation of the backend can be found in the [top-level docs](../docs/) directory. 
