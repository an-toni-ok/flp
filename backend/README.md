# Backend

This directory contains the backend part of the flp web application.
It consists of a Flask web application, a Celery instance for running background tasks and a Redis Server, which is working as a message broker between Flask and Celery.

## Setup

The easiest way to setup the backend is by using docker compose. If you do not have docker installed, you can follow the [official installation instructions](https://docs.docker.com/get-docker/).
You also need to install docker compose, to do so you can follow the [official installation instructions](https://docs.docker.com/compose/install/).

To start the backend applications, simply execute the following command in this directory and wait a few seconds.

```bash
docker compose up
```

You can now access the Flask web application at http://localhost:5000 (and at http://172.0.0.1:5000) and the Redis Insights at http://localhost:8001 (and at http://172.0.0.1:8001).
