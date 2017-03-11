# config.py

import os
# from common.constants import INSTANCE_FOLDER_PATH


class BaseConfig(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = os.environ['DEBUG']
    DB_NAME = os.environ['DB_NAME']
    DB_USER = os.environ['DB_USER']
    DB_PASS = os.environ['DB_PASS']
    DB_SERVICE = os.environ['DB_SERVICE']
    DB_PORT = os.environ['DB_PORT']
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        DB_USER, DB_PASS, DB_SERVICE, DB_PORT, DB_NAME
    )
    SECRET_KEY = os.environ['SECRET_KEY']
    SECURITY_PASSWORD_HASH = os.environ['SECURITY_PASSWORD_HASH']
    SECURITY_PASSWORD_SALT = os.environ['SECURITY_PASSWORD_SALT']
    DEFAULT_ADMIN_USER = os.environ['DEFAULT_ADMIN_USER']
    DEFAULT_ADMIN_PASSWORD = os.environ['DEFAULT_ADMIN_PASSWORD']

class DefaultConfig(BaseConfig):

   # Statement for enabling the development environment
   #DEBUG = True
   pass
