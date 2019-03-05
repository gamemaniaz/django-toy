FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /middleware-louis

WORKDIR /middleware-louis

ADD . /middleware-louis/

RUN pip install -r requirements.txt
