# syntax=docker/dockerfile:1

# Setup the celery worker
FROM python:3.10-slim-buster

WORKDIR /backend

# Install the backend requirements
COPY backend/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy the backend code
COPY backend/ .

# Copy the optimization package into the backend
COPY optimization/ ./server/optimization

# Install the optimization requirements
RUN pip3 install -r server/optimization/requirements.txt

CMD celery -A make_celery worker --loglevel INFO