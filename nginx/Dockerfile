# https://hub.docker.com/_/nginx/
FROM nginx:1-alpine
MAINTAINER drad <drader@adercon.com>

# NOTE: the following is only needed for develop/debug purposes.
RUN apk add --no-cache bash

RUN rm /etc/nginx/conf.d/default.conf
ADD conf.d/flask_project.conf /etc/nginx/conf.d/

# create dir for ssl certs.
RUN mkdir -p /etc/nginx/ssl
ADD ssl/nginx.* /etc/nginx/ssl/
