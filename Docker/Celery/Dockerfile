# syntax=docker/dockerfile:1

# Setup the celery worker
FROM python:3.10-slim-buster

WORKDIR /backend

# Install the backend requirements
COPY backend/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Install the optimization requirements
COPY optimization/requirements.txt ./server/optimization/requirements.txt
RUN pip3 install -r server/optimization/requirements.txt

# Copy the backend code
COPY backend/ .

# Copy the optimization package into the backend
COPY optimization/ ./server/optimization

CMD celery -A make_celery worker --loglevel INFO