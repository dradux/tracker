# README.md

TRTrack is the Test Result Tracker.


## TODO
- change web container to use alpine over ONBUILD
- get admin piece setup


## Stack
- web: nginx
- app: flask + admin, gunicorn, sqlalchemy
- db: postgres


## Setup
- build containers: `docker-compose build`
- create db table: `docker-compose run web /usr/local/bin/python create_db.py`


## Run
- start: `docker-compose up`
- use: `http://localhost`


## Attribution
- [dockerize base](https://realpython.com/blog/python/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud/)
- [flask-admin base](https://github.com/flask-admin/flask-admin/blob/master/examples/sqla/app.py)
