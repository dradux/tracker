# app.py

import sys
import os
import os.path as op
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
#~ from flask.ext.security import login_required, Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, utils
from flask.ext.security import login_required, Security, SQLAlchemyUserDatastore, utils
import flask_admin as admin
from config import BaseConfig

# Create application
app = Flask(__name__)
app.config.from_object(BaseConfig)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'W/]TUmc`YX]|<-sr+he&"1M*3{T9|SB|Q'
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
app.config['SECURITY_PASSWORD_SALT'] = 'mySaltWillGoHERE123A23'

db = SQLAlchemy(app)

from models import *
from views import *

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.before_first_request
def before_first_request():
    # Create any database tables that don't exist yet.
    db.create_all()

    # Create the Roles "admin" and "user" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='user', description='User')

    encrypted_password = utils.encrypt_password('Q832Qs~QO487GTGh6QWC')
    if not user_datastore.get_user('admin@trtrack'):
        user_datastore.create_user(name='admin', username='admin', email='admin@trtrack', password=encrypted_password)

    # Commit any database changes; the User and Roles must exist before we can add a Role to the User
    db.session.commit()

    # assign roles
    user_datastore.add_role_to_user('admin@trtrack', 'admin')
    user_datastore.add_role_to_user('admin@trtrack', 'user')

    db.session.commit()

@app.route('/')
@login_required
def index():
    return render_template('index.html')

# Create admin
admin = admin.Admin(app, name='TRTrack', template_mode='bootstrap3', index_view=HomeView(name='Home'))

# Add views
admin.add_view(UserAdmin(User, db.session))
admin.add_view(ServerView(Server, db.session))
admin.add_view(TestResultView(TestResult, db.session))
admin.add_view(OnlineHelpView(name='Online Help', endpoint='online_help', category='Help'))
admin.add_view(AboutView(name='About', endpoint='help_about', category='Help'))


if __name__ == '__main__':
    app_dir = op.realpath(os.path.dirname(__file__))
    # Start app
    app.run(debug=True)
