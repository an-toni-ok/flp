# FLP <!-- omit in toc -->

This folder contains the flp webapplication consisting of a frontend, backend and optimization console program. It's purpose is the optimization of production layouts. The user can draw a factory plan in 2D with free and restricted spaced, input an ordered list of production processes and a list of choosable machines for the factory and configure optimization parameters. From this information several optimized production layouts will be generated, which are displayed on the factory plan with additional information, e.g. the cost per piece and the worker alloted to a machine, being displayed on the side.

## Contents <!-- omit in toc -->

- [Setup](#setup)
  - [Installation](#installation)
  - [Development](#development)
- [Application structure](#application-structure)
- [Documentation](#documentation)

## Setup

### Installation

Note: The following command should not be used if you changed the source code. Use the instructions [here](#development) instead

To start the backend applications for the production server, simply execute the following command in this directory and wait a few seconds.

```bash
docker compose --profile app up
```

The executed command now automatically starts the containers for Flask, Celery in Redis in the correct sequence. As soon as the start of the containers is completed will you be able to access the Flask web application at http://localhost:5000 (and at http://172.0.0.1:5000) and the Redis Insights at http://localhost:8001 (and at http://172.0.0.1:8001).

### Development

To update the code used in the production server (either the Flask code or the Celery Tasks), a new docker image needs to be generated and used by docker compose. 

Simply execute the following command if the code has changed:

```bash
docker compose --profile app up --build
```

## Application structure

The application is split into the following three applications:
- Frontend: The UI implemented as a SPA (Single-Page Application) in vue in the directory [frontend](./frontend/).
- Backend: The server, a Flask Application in the directory [backend](./backend/). It contains the logic for the Web Server and for Celery tasks that are executed on a dedicated Celery worker, but callable from the Flask server. 
- Optimization: The optimization programm in the directory [optimization](./optimization/)

The three parts are connected by using Dockerfile for [Celery](./Docker/Celery/Dockerfile) and [Flask](./Docker/Flask/Dockerfile) to create images with the different applications placed into the right places, e.g. in the Flask Dockerfile the Frontend SPA is compiled into static files which are afterwards placed at the correct location within the Flask Application. [Docker compose](./docker-compose.yaml) is used to jointly orchestrate all the containers allowing a start with a single command.

## Documentation

The application is documented in the [docs](./docs/) directory and the subsystems of the application contain short README Files in their directories.
