# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY .. /code/

# TODO nie trzeba tych 3 lini jednak
RUN pwd; \
    cd django-playground/my_tennis_club; \
    pwd
