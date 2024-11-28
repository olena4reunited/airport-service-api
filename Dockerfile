FROM python:3.12.6-alpine3.20
LABEL authors="olena.cherneha4@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN adduser \
    --disabled-password \
    --no-create-home \
    airport_user

USER airport_user
