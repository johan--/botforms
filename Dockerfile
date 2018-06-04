FROM python:2.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

RUN apt-get update && apt-get install -y default-jdk

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 80:5000
