# app.py

import sys
import os
import os.path as op
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask.ext.security import login_required, Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, utils
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

    # Create the Roles "admin" and "end-user" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='user', description='User')

    # Create two Users for testing purposes -- unless they already exists.
    # In each case, use Flask-Security utility function to encrypt the password.
    encrypted_password = utils.encrypt_password('password')
    if not user_datastore.get_user('user@example.com'):
        user_datastore.create_user(email='user@example.com', password=encrypted_password)
    if not user_datastore.get_user('drader@adercon.com'):
        user_datastore.create_user(email='drader@adercon.com', password=encrypted_password)

    # Commit any database changes; the User and Roles must exist before we can add a Role to the User
    db.session.commit()

    # Give one User has the "user" role, while the other has the "admin" role. (This will have no effect if the
    # Users already have these Roles.) Again, commit any database changes.
    user_datastore.add_role_to_user('user@example.com', 'user')
    user_datastore.add_role_to_user('drader@adercon.com', 'admin')
    user_datastore.add_role_to_user('drader@adercon.com', 'user')
    db.session.commit()


# Flask views
#~ @app.route('/')
#~ def index():
    #~ return '<a href="/admin/">To Admin...</a>'

#~ @app.route('/home')
#~ @login_required
#~ def home():
    #~ return render_template('templates/index.html')

@app.route('/')
@login_required
def index():
    return render_template('index.html')

# Create admin
#admin = admin.Admin(app, name='Example: SQLAlchemy', template_mode='bootstrap3')
admin = admin.Admin(app, name='TRTrack', template_mode='bootstrap3', index_view=HomeView(name='Home'))

# Add views
#~ admin.add_view(sqla.ModelView(User, db.session))
admin.add_view(UserAdmin(User, db.session))
#~ admin.add_view(sqla.ModelView(Tag, db.session))
#~ admin.add_view(PostAdmin(db.session))
#~ admin.add_view(TreeView(Tree, db.session))
admin.add_view(ServerView(Server, db.session))
admin.add_view(TestResultView(TestResult, db.session))
admin.add_view(HelpView(name='Online Help', endpoint='online-help', category='Help'))
admin.add_view(HelpView(name='About', endpoint='about', category='Help'))


if __name__ == '__main__':
    # Build a sample db on the fly, if one does not exist yet.
    app_dir = op.realpath(os.path.dirname(__file__))
    #database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    #if not os.path.exists(database_path):
    #    build_sample_db()
    #sys.stdout.write('BUILDING SAMPLE DB...')
    #build_sample_db()
    #sys.stdout.write('SAMPLE DB BUILT!')

    # Start app
    app.run(debug=True)
