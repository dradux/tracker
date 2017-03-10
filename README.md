# README.md

TRTrack is the Test Result Tracker.


## TODO
- change web container to use alpine over ONBUILD
- need migrations support
  * /add 'user' to server and test_results models
  * should we add 'project' structure?
- final cleanup
- /add appropriate .Dockerignore
- move configs to config.py file and structure...
- /add live-reload for flask app code changes
- /add a 'created_at' dts to test_results
- move views to individual classes
- move models to individual classes

## Stack
- web: nginx
- app: flask + admin, gunicorn, sqlalchemy
- db: postgres


## Setup
- build containers: `docker-compose build`
- create db tables
  * start db container: `docker-compose up -d postgres`
  * create tables: `docker-compose run web python create_db.py`
- load db with data (optional): `docker-compose run web python load_db.py`


## Run
- start: `docker-compose up`
- use: `http://localhost`

## Development
- init migrations: `docker-compose run web python manage.py db init`
- create migration: `docker-compose run web python manage.py db migrate`
- apply migration: `docker-compose run web python manage.py db upgrade`

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
- [https://realpython.com/blog/python/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/] - migrations setup and usage guide
