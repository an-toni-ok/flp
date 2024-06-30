# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /backend

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD celery -A make_celery worker --loglevel INFO