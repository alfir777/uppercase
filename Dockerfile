FROM python:3.12.8-slim-bookworm

RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean

RUN addgroup --system --gid 2000 user && adduser --system --uid 2000 user

WORKDIR /app

COPY ./pyproject.toml /app/pyproject.toml
COPY ./poetry.lock /app/poetry.lock

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root --only main

COPY ./entrypoint.sh /app
COPY src /app

RUN chown -R user:user /app

USER user