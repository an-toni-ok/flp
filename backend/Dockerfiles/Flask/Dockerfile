# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /backend

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./server ./server

EXPOSE 5000

CMD flask --app server run --host="0.0.0.0"