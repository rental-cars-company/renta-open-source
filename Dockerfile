# Declare the argument first
ARG PRIME_IMAGE_NAME

FROM 075846067979.dkr.ecr.us-east-1.amazonaws.com/rent-car-backend:${PRIME_IMAGE_NAME} AS base

WORKDIR /moshin_backend

RUN rm -r /moshin_backend/*

COPY moshin_backend/ .
COPY pyproject.toml poetry.lock ./

EXPOSE 8000