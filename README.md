# README.md

TRTrack is the Test Result Tracker.


## TODO
- change web container to use alpine over ONBUILD
- /get admin piece setup
- /add authentication
- /add user to server and test_results data
- /fix stability issue (for some reason data just goes away)
- need migrations support
- /move admin views to views class or dir
- final cleanup


## Stack
- web: nginx
- app: flask + admin, gunicorn, sqlalchemy
- db: postgres


## Setup
- build containers: `docker-compose build`
- create db tables
  * start db container: `docker-compose up -d postgres`
  * create tables: `docker-compose run web /usr/local/bin/python create_db.py`
- load db with data (optional): `docker-compose run web /usr/local/bin/python load_db.py`


## Run
- start: `docker-compose up`
- use: `http://localhost`


## Attribution
- [dockerize base](https://realpython.com/blog/python/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud/)
- [flask-admin base](https://github.com/flask-admin/flask-admin/blob/master/examples/sqla/app.py)

## Links
- [https://github.com/mrjoes/flask-admin/blob/master/doc/quickstart.rst](flask-admin quickstart)
- [https://github.com/mattupstate/flask-security-example/blob/master/app.py](flask-security-example)
- [https://github.com/sasaporta/flask-security-admin-example/blob/master/main.py](flask-security-admin-example) - the good one
- [https://pythonhosted.org/Flask-Security/quickstart.html](flask-security)
- [http://flask-admin.readthedocs.io/en/latest/introduction/](flask-admin intro)
- [http://examples.flask-admin.org/](flask-admin examples)
