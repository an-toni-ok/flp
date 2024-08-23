# syntax=docker/dockerfile:1

# Build the frontend static files.
FROM node:20.17 as build-stage

WORKDIR /frontend

COPY frontend .

RUN npm install
RUN npm run build

# Setup the backend server
FROM python:3.10-slim-buster

WORKDIR /backend

# Install the backend requirements
COPY backend/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

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

# Install the optimization requirements
RUN pip3 install -r server/optimization/requirements.txt

# Expose the port
EXPOSE 5000

# Set the start command
CMD flask --app server run --host="0.0.0.0"