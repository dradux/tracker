# README.md

TRacker is a Test Result tracker. If you use jmeter, locust.io, or another tool/app to test applications TRacker provides a quick place to record and share test results.

TRacker started as a replacement for using an Excel spreadsheet to track test results. Excel worked to track test results; however, it was difficult to pass around a spreadsheet to different team members and ensure all results were in the "final" copy. TRacker addressed this issue by providing a central location all members can use simultaneously without adding a lot of burden.

TRacker is designed to be easy to setup and easy to use. TRacker supports multiple test plans and servers; however, tracker does not have a concept of a project. For example, imagine you have Application A which is a web app with multiple interfaces, services, and components. TRacker supports multiple test plans which allows you to have one test plan that tests component A, component B, and component C of Application A. Now imagine you have Application B which has its own interfaces, services, and components. You can add new test plans, servers, and then record Test Results for Application B; however, TRacker does not segregate this information. All users will be able to see test plans, servers, and test results for Application A and Application B. This may present an issue if you have stakeholders of one Application who should not see data from the other Application.

The above issue of segregating Application A from Application B can easily be handled by simply running seperate instances of TRacker as tracker runs inside of docker containers. The process to run multiple instances of TRacker is simple:

- For Application A
  * `cd /opt/projects && git clone https://github.com/dradux/tracker.git application_a && cd application_a && docker-compose build && docker-compose up -d`
- For Application B
  * `cd /opt/projects && git clone https://github.com/dradux/tracker.git application_b && cd application_b && docker-compose build && docker-compose up -d`

You now have two instances of TRacker, each completely separate from the other!


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
- create migration (autodetect changes): `docker-compose run web python manage.py db migrate -m "concise desc of change"`
- create migration (manually): `docker-compose run web python manage.py db revision -m "add test_result_status items"`
- apply migration: `docker-compose run web python manage.py db upgrade`
- rollback migration: `docker-compose run web python manage.py db downgrade`
- view migration history: `docker-compose run web python manage.py db history`
- get current version: `docker-compose run web python manage.py db current --verbose`

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
