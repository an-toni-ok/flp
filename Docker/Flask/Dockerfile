# syntax=docker/dockerfile:1

# Install the backend requirements
# This is done here so that it only needs to run again
# if the requirements change.
FROM python:3.10-slim-buster AS python-prep

WORKDIR /backend

# Install the backend requirements
COPY backend/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Install the optimization requirements
COPY optimization/requirements.txt ./server/optimization/requirements.txt
RUN pip3 install -r server/optimization/requirements.txt

# Build the frontend static files.
FROM node:20.17 AS build-stage

WORKDIR /frontend

COPY frontend/package.json ./package.json
RUN npm install

COPY frontend .
RUN npm run build

# Setup the backend server
FROM python-prep

# Copy the backend code
COPY backend/server ./server

# Copy the frontend static files into the backend
COPY --from=build-stage /frontend/dist/assets/index*.js server/static/index.js
COPY --from=build-stage /frontend/dist/assets/index*.css server/static/index.css

# Copy the optimization package into the backend
#
# This code is not used in the backend itself, but since the
# celery tasks are code included in the backend
# server the package needs to be present for everything to
# workd
COPY optimization/ ./server/optimization

# Expose the port
EXPOSE 5000

# Set the start command
CMD flask --app server run --host="0.0.0.0"