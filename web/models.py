# models.py
import datetime
from app import db

from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

#
# Extended with example from: https://github.com/flask-admin/flask-admin/blob/master/examples/sqla/app.py
#

#~ class User(db.Model):
    #~ __tablename__ = 'ex_user'
    #~ id = db.Column(db.Integer, primary_key=True)
    #~ first_name = db.Column(db.String(100))
    #~ last_name = db.Column(db.String(100))
    #~ username = db.Column(db.String(80), unique=True)
    #~ email = db.Column(db.String(120), unique=True)

    #~ def __str__(self):
        #~ return self.username


# Create M2M table
#~ post_tags_table = db.Table('post_tags', db.Model.metadata,
                           #~ db.Column('post_id', db.Integer, db.ForeignKey('ex_post.id')),
                           #~ db.Column('tag_id', db.Integer, db.ForeignKey('ex_tag.id'))
                           #~ )


#~ class Post(db.Model):
    #~ __tablename__ = 'ex_post'
    #~ id = db.Column(db.Integer, primary_key=True)
    #~ title = db.Column(db.String(120))
    #~ text = db.Column(db.Text, nullable=False)
    #~ date = db.Column(db.DateTime)

    #~ user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    #~ user = db.relationship(User, backref='ex_posts')

    #~ tags = db.relationship('Tag', secondary=post_tags_table)

    #~ def __str__(self):
        #~ return self.title


#~ class Tag(db.Model):
    #~ __tablename__ = 'ex_tag'
    #~ id = db.Column(db.Integer, primary_key=True)
    #~ name = db.Column(db.Unicode(64))

    #~ def __str__(self):
        #~ return self.name


#~ class UserInfo(db.Model):
    #~ __tablename__ = 'ex_userinfo'
    #~ id = db.Column(db.Integer, primary_key=True)

    #~ key = db.Column(db.String(64), nullable=False)
    #~ value = db.Column(db.String(64))

    #~ user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    #~ user = db.relationship(User, backref='info')

    #~ def __str__(self):
        #~ return '%s - %s' % (self.key, self.value)


#~ class Tree(db.Model):
    #~ __tablename__ = 'ex_tree'
    #~ id = db.Column(db.Integer, primary_key=True)
    #~ name = db.Column(db.String(64))
    #~ parent_id = db.Column(db.Integer, db.ForeignKey('ex_tree.id'))
    #~ parent = db.relationship('Tree', remote_side=[id], backref='children')

    #~ def __str__(self):
        #~ return self.name

#
# Test Result Models
#
class Server(db.Model):
    __tablename__ = 'server'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cpu_cores = db.Column(db.Integer, nullable=False)
    compute_units = db.Column(db.Numeric(5,1), nullable=True)
    memory = db.Column(db.Numeric(5,1), nullable=False)
    virtual = db.Column(db.Boolean, nullable=False, default=True)
    storage = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship("User", foreign_keys=[creator_id])

    def __str__(self):
        fmt_compute_units=''
        if self.compute_units:
            fmt_compute_units='%scu/' % (self.compute_units)
        return '%s (%scores/%s%smemory)' % (self.name, self.cpu_cores, fmt_compute_units, self.memory)

class TestResult(db.Model):
    __tablename__ = 'test_result'
    id = db.Column(db.Integer, primary_key=True)
    test_date = db.Column(db.DateTime, nullable=False)
    test_plan = db.Column(db.String(200), nullable=False)
    #test_source = db.Column(db.String(100), nullable=False)
    #test_target = db.Column(db.String(100), nullable=False)

    source_server_id = db.Column(db.Integer(), db.ForeignKey('server.id'), nullable=False)
    source_server = db.relationship("Server", foreign_keys=[source_server_id])

    target_server_id = db.Column(db.Integer(), db.ForeignKey('server.id'), nullable=False)
    target_server = db.relationship(Server, foreign_keys=[target_server_id])

    app_version = db.Column(db.String(15), nullable=True)
    number_users = db.Column(db.Integer, nullable=False)
    ramp_up = db.Column(db.Integer, nullable=False)

    run_length = db.Column(db.Integer, nullable=True)
    number_failures = db.Column(db.Integer, nullable=True)
    number_requests = db.Column(db.Integer, nullable=True)
    average_response_time = db.Column(db.Integer, nullable=True)

    target_server_cpu = db.Column(db.Numeric(5,2), nullable=True)
    target_server_memory = db.Column(db.Numeric(5,2), nullable=True)
    target_server_load = db.Column(db.Numeric(5,2), nullable=True)

    test_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship("User", foreign_keys=[creator_id])

    def __str__(self):
        return '%s (%s)' % (self.test_plan, test_date)


#
# Flask-Security Models
#
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # __str__ is required by Flask-Admin, so we can have human-readable values for the Role when editing a User.
    # If we were using Python 2.7, this would be __unicode__ instead.
    def __str__(self):
        return self.name

    # __hash__ is required to avoid the exception TypeError: unhashable type: 'Role' when saving a User
    def __hash__(self):
        return hash(self.name)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(33), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    note = db.Column(db.Text, nullable=True)

    def __str__(self):
        #~ return '<User id=%s email=%s>' % (self.id, self.email)
        return '%s' % (self.username)
