# app.py

import sys
import os
import logging
from logging.handlers import RotatingFileHandler

import os.path as op
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask.ext.security import login_required, Security, SQLAlchemyUserDatastore, utils
import flask_admin as admin
from config import BaseConfig
import config as Config

# Create application
app = Flask(__name__)
app.config.from_object(BaseConfig)

db = SQLAlchemy(app)

from models import *
from views import *

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

#~ @TODO: find a better way as the following causes issues with flex-migrate.
#~
#~ @app.before_first_request
#~ def before_first_request():
    #~ # Create any database tables that don't exist yet.
    #~ db.create_all()

    #~ #app.logger.info('### NOTICES ###')
    #~ app.logger.debug('* setting DEFAULT_ADMIN_USER: %s' % (Config.DefaultConfig.DEFAULT_ADMIN_USER))
    #~ app.logger.debug('* setting DEFAULT_ADMIN_PASSWORD: %s' % (Config.DefaultConfig.DEFAULT_ADMIN_PASSWORD))

    #~ # Create the Roles "admin" and "user" -- unless they already exist
    #~ user_datastore.find_or_create_role(name='admin', description='Administrator')
    #~ user_datastore.find_or_create_role(name='user', description='User')

    #~ encrypted_password = utils.encrypt_password(Config.DefaultConfig.DEFAULT_ADMIN_PASSWORD)
    #~ app.logger.debug('- encrypted_password: %s' % (encrypted_password))
    #~ if not user_datastore.get_user(Config.DefaultConfig.DEFAULT_ADMIN_USER):
        #~ user_datastore.create_user(name='admin', username='admin', email=Config.DefaultConfig.DEFAULT_ADMIN_USER, password=encrypted_password)

    #~ # Commit any database changes; the User and Roles must exist before we can add a Role to the User
    #~ db.session.commit()

    #~ # assign roles
    #~ user_datastore.add_role_to_user(Config.DefaultConfig.DEFAULT_ADMIN_USER, 'admin')
    #~ user_datastore.add_role_to_user(Config.DefaultConfig.DEFAULT_ADMIN_USER, 'user')

    #~ db.session.commit()

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/logout')
def logout_view():
    login.logout_user()
    return redirect(url_for('admin.index'))

@app.route('/change_password')
def change_password():
    return render_template('security/change_password.html')

# Create admin
admin = admin.Admin(app, name='TRacker', template_mode='bootstrap3', index_view=HomeView(name='Home'))

# Add views
admin.add_view(TestResultView(TestResult, db.session, name='Test Results'))

admin.add_view(RunMetricView(RunMetric, db.session, name='Run Metrics', category='Config'))
admin.add_view(ServerView(Server, db.session, name='Servers', category='Config'))
admin.add_view(TestResultStatusView(TestResultStatus, db.session, name='Statuses', category='Config'))
admin.add_view(TestPlanView(TestPlan, db.session, name='Test Plans', category='Config'))
admin.add_view(UserAdmin(User, db.session, name='Users', category='Config'))

#admin.add_view(AccountLogoutView(name='Logout', endpoint='account_logout', category='Account'))
admin.add_view(AccountView(name='User', endpoint='account_user', category='Account'))
admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))
admin.add_link(LoginMenuLink(name='Login', category='', url="/login"))



admin.add_view(OnlineHelpView(name='Online Help', endpoint='online_help', category='Help'))
admin.add_view(AboutView(name='About', endpoint='help_about', category='Help'))


if __name__ == '__main__':
    app_dir = op.realpath(os.path.dirname(__file__))
    # Start app
    app.run(debug=True)
