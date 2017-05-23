# https://hub.docker.com/_/nginx/
FROM nginx:1-alpine
MAINTAINER drad <drader@adercon.com>

#ARG SERVER_URL

# NOTE: the following is only needed for develop/debug purposes.
RUN apk add --no-cache bash

RUN rm /etc/nginx/conf.d/default.conf
ADD conf.d/flask_project.conf /etc/nginx/conf.d/

# replace #SERVER_URL# with the SERVER_URL from .env file
#RUN sed -i "s/#SERVER_URL#/${SERVER_URL}/g" /etc/nginx/conf.d/flask_project.conf

# create dir for ssl certs.
RUN mkdir -p /etc/nginx/ssl
ADD ssl/nginx.* /etc/nginx/ssl/
