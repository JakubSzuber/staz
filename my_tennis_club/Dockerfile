FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y iputils-ping  # Install ping utility

COPY .. /code/
