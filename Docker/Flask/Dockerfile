# syntax=docker/dockerfile:1

# Build the frontend static files.
FROM node:20 as build-stage

WORKDIR /frontend

COPY frontend .

RUN npm install
RUN npm run build

FROM python:3.10-slim-buster

WORKDIR /backend

COPY backend/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY backend/server ./server
COPY --from=build-stage /frontend/dist/assets/index*.js server/static/index.js
COPY --from=build-stage /frontend/dist/assets/index*.css server/static/index.css

EXPOSE 5000

CMD flask --app server run --host="0.0.0.0"