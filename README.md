# README.md

TRacker is the Test Result Tracker!


## TODO
- add "type" column to test plan (e.g. jmeter, locust, etc.)
- add logic that introspects the test plan and grabs summary, details, run info, etc. if possible
- add db backups


## Stack
- web: nginx
- app: flask + admin, gunicorn, sqlalchemy
- db: postgres


## Setup
- generate or deploy SSL Certs (see HTTPS section below)
- copy the `.env.template` to `.env` and edit accordingly
- build containers: `docker-compose build`
- apply latest db updates: `docker-compose run web python manage.py db upgrade`



## Run
- start: `docker-compose up`
- use: `http://localhost`


## HTTPS
This webapp uses authentication (username/password), you should always use SSL when authenticating to ensure the username/password are not captured by MITM.

If you have certs, place them in the `nginx/ssl` directory (either change your certs to be named as the current certs `nginx.crt` and nginx.key` or update the `conf.d/flask_project.conf` to reflect the new names of your certs).

If you do not have certs, you can generate your own self-signed certs as follows:
- from the project root: `sudo openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout nginx/ssl/nginx.key -out nginx/ssl/nginx.crt`
  * answer the questions as prompted
  * after all questions have been answered you are done (build and restart your container)

Note that the app starts up port 80 and 443, the `flask_project.conf` (nginx conf file) redirects port 80 traffic to port 443.


## Development
- init migrations: `docker-compose run web python manage.py db init`
- create migration: `docker-compose run web python manage.py db migrate`
- apply migration: `docker-compose run web python manage.py db upgrade`


## Notes
- the access/error logs from nginx are wrote to the nginx/logs volume to persist them and to allow easy monitoring of these files.


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
