# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

#COPY .env .
## Use environment variables
#ENV AWS_ACCESS_KEY_1=$AWS_ACCESS_KEY_ID
#ENV AWS_ACCESS_KEY_2=$AWS_ACCESS_KEY_VALUE

#RUN mkdir ~/.aws && echo "[default]" > ~/.aws/credentials && echo "aws_access_key_id = "$AWS_ACCESS_KEY_ID"" >> ~/.aws/credentials && echo "aws_secret_access_key = "$AWS_ACCESS_KEY_VALUE"" >> ~/.aws/credentials;
#RUN echo "[default]" > ~/.aws/config && echo "region = "eu-central-1"" >> ~/.aws/config && chmod 777 ~/.aws/config;

CMD ["uvicorn", "gen_description:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
