# https://hub.docker.com/_/python/
FROM python:3.6-alpine
# FROM python:3.4-onbuild   #you can use -onbuild if you dont want alpine-linux
MAINTAINER drad <drader@adercon.com>

# create the app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# NOTE: the following is only needed for develop/debug purposes
#RUN apk add --no-cache bash

# the following are needed to build psycopg2
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev

# copy requirements.txt file so we can build container
#  note: at runtime we use a volume, not container-based code.
COPY ./requirements.txt /
# install project requirements
RUN pip install -r /requirements.txt
