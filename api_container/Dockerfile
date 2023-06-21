## Python lightweight alpine image
FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

## Create the group and user in order to later use a non-root user and give him permission to workdir. Furthermore, install needed commands
RUN addgroup -g 1000 python \
      && adduser -u 1000 -G python -s /bin/sh -D python;  \
    mkdir /code \
      && chown -R python:python /code; \
    apk update; \
    apk add --no-cache bash; \
    apk add --no-cache tree; \
    apk add --no-cache iputils; \
    apk add --no-cache curl;

## Use /code as a working directory
WORKDIR /code

## Copy pip dependencies to workdir
COPY requirements.txt /code/

## Instal pip dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

## Copy all files to workdir
COPY . /code/

#COPY .env .
## Use environment variables
#ENV AWS_ACCESS_KEY_1=$AWS_ACCESS_KEY_ID
#ENV AWS_ACCESS_KEY_2=$AWS_ACCESS_KEY_VALUE

#RUN mkdir ~/.aws && echo "[default]" > ~/.aws/credentials && echo "aws_access_key_id = "$AWS_ACCESS_KEY_ID"" >> ~/.aws/credentials && echo "aws_secret_access_key = "$AWS_ACCESS_KEY_VALUE"" >> ~/.aws/credentials;
#RUN echo "[default]" > ~/.aws/config && echo "region = "eu-central-1"" >> ~/.aws/config && chmod 777 ~/.aws/config;

## Switch to non-root user
USER python:python

# Run Uvicorn service
CMD ["uvicorn", "gen_description:app", "--host", "0.0.0.0", "--port", "80", "--reload"]

## Healthchecks
HEALTHCHECK --interval=120s --timeout=5s --start-period=20s --retries=3 \
    CMD curl --fail http://localhost:80/health || exit 1
