# models.py
import datetime
from app import db
from flask.ext.security import UserMixin, RoleMixin

class TestResultStatus(db.Model):
    __tablename__ = 'test_result_status'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(13), nullable=False)

    def __str__(self):
        return '%s' % (self.status)


class Server(db.Model):
    __tablename__ = 'server'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(13), nullable=False)
    full_name = db.Column(db.String(100), nullable=True)
    version = db.Column(db.Integer, nullable=True)
    active = db.Column(db.Boolean, nullable=True, default=True)
    cpu_cores = db.Column(db.Integer, nullable=False)
    compute_units = db.Column(db.Numeric(5,1), nullable=True)
    memory = db.Column(db.Numeric(5,1), nullable=False)
    virtual = db.Column(db.Boolean, nullable=False, default=True)
    storage = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship("User", foreign_keys=[creator_id])

    def __str__(self):
        #fmt_compute_units=''
        #if self.compute_units:
        #    fmt_compute_units='%su/' % (self.compute_units)
        fmt_version=''
        if self.version:
            fmt_version='(v.%s)' % (self.version)
        # format: "Server (v.0)"
        return '%s %s' % (self.name, fmt_version)


class TestPlan(db.Model):
    __tablename__ = 'test_plan'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(10), nullable=False)
    source_url = db.Column(db.String, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    run_info = db.Column(db.Text, nullable=False)
    dependencies = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship("User", foreign_keys=[creator_id])

    def __str__(self):
        # format: "chem4 (v1.0.0)"
        return '%s (v%s)' % (self.name, self.version)


server_testresults = db.Table('server_testresults',
                              db.Column('testresult_id', db.Integer(), db.ForeignKey('test_result.id')),
                              db.Column('server_id', db.Integer(), db.ForeignKey('server.id')))

target_serverrunmetric_testresults = db.Table('target_serverrunmetric_testresults',
                              db.Column('testresult_id', db.Integer(), db.ForeignKey('test_result.id')),
                              db.Column('server_run_metric_id', db.Integer(), db.ForeignKey('server_run_metric.id')))

class TestResult(db.Model):
    __tablename__ = 'test_result'
    id = db.Column(db.Integer, primary_key=True)
    test_date = db.Column(db.DateTime, nullable=False)
    status_id = db.Column(db.Integer(), db.ForeignKey('test_result_status.id'), nullable=True)
    status = db.relationship("TestResultStatus", foreign_keys=[status_id])

    test_plan_id = db.Column(db.Integer(), db.ForeignKey('test_plan.id'), nullable=False)
    test_plan = db.relationship("TestPlan", foreign_keys=[test_plan_id])

    # @TODO: only allow 'active' servers.
    source_servers = db.relationship('Server', secondary=server_testresults,
                                     backref=db.backref('test_result', lazy='dynamic'))

    target_server_id = db.Column(db.Integer(), db.ForeignKey('server.id'), nullable=False)
    target_server = db.relationship(Server, foreign_keys=[target_server_id])

    run_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    run_by = db.relationship("User", foreign_keys=[run_by_id])

    app_version = db.Column(db.String(15), nullable=True)
    number_users = db.Column(db.Integer, nullable=False)
    ramp_up = db.Column(db.Integer, nullable=False)
    loop_amount = db.Column(db.Integer, nullable=True)

    run_length = db.Column(db.Integer, nullable=True)
    number_failures = db.Column(db.Integer, nullable=True)
    number_requests = db.Column(db.Integer, nullable=True)
    average_response_time = db.Column(db.Integer, nullable=True)

    # multiple occurring TargetServerRunMetrics
    target_server_run_metrics = db.relationship('ServerRunMetric', secondary=target_serverrunmetric_testresults,
                                     backref=db.backref('test_result', lazy='dynamic'))
    target_server_run_metrics_url = db.Column(db.String(1333), nullable=True)

    prerun_notes = db.Column(db.Text, nullable=True)
    run_notes = db.Column(db.Text, nullable=True)
    postrun_notes = db.Column(db.Text, nullable=True)
    failure_notes = db.Column(db.Text, nullable=True)
    test_notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship("User", foreign_keys=[creator_id])

    def __str__(self):
        return '%s (%s)' % (self.test_plan, self.test_date)


class RunMetric(db.Model):
    __tablename__ = 'run_metric'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(33), nullable=False)
    note = db.Column(db.Text, nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship("User", foreign_keys=[creator_id])

    def __str__(self):
        return '%s' % (self.name)


class ServerRunMetric(db.Model):
    __tablename__ = 'server_run_metric'
    id = db.Column(db.Integer, primary_key=True)
    run_metric_id = db.Column(db.Integer(), db.ForeignKey('run_metric.id'), nullable=False)
    run_metric = db.relationship(RunMetric, foreign_keys=[run_metric_id])

    value = db.Column(db.Numeric(5,2), nullable=False)
    note = db.Column(db.Text, nullable=True)

    def __str__(self):
        return '%s:%s' % (self.run_metric, self.value)


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
