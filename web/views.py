# views.py

from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from flask.ext.admin import Admin, BaseView, expose, AdminIndexView
from flask.ext.security import current_user, utils
from wtforms import validators
from wtforms.fields import PasswordField

from jinja2 import Markup
from flask import url_for


#from flask_admin.contrib.sqla.filters import BaseSQLAFilter, FilterEqual
from models import Server

# custom filter for Server: only active servers.
#~ class FilterActiveServer(BaseSQLAFilter):
    #~ def apply(self, query, value, alias=None):
        #~ if value:
            #~ return query.filter(self.column == True)
        #~ else:
            #~ return query.filter(self.column == False)

    #~ def operation(self):
        #~ return 'is Active'

class HomeView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('home.html')

class OnlineHelpView(BaseView):
    @expose('/')
    def index(self):
        return self.render('help-online.html')

class AboutView(BaseView):
    @expose('/')
    def index(self):
        return self.render('help-about.html')

# Customized User model for SQL-Admin
class UserAdmin(sqla.ModelView):

    #can_view_details = True
    #details_modal = True

    # default sort by name
    column_default_sort = ('name', False)

    # Don't display the password on the list of Users
    column_exclude_list = ('password',)

    column_searchable_list = ['email']

    # Don't include the standard password field when creating or editing a User (but see below)
    form_excluded_columns = ('password',)

    # Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True

    def _note_formatter(view, context, model, name):
        return Markup("%s" % (model.note)) if model.note else ""

    column_formatters = {
        'note': _note_formatter,
    }

    # Prevent administration of Users unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')

    # On the form for creating or editing a User, don't display a field corresponding to the model's password field.
    # There are two reasons for this. First, we want to encrypt the password before storing in the database. Second,
    # we want to use a password field (with the input masked) rather than a regular text field.
    def scaffold_form(self):

        # Start with the standard form as provided by Flask-Admin. We've already told Flask-Admin to exclude the
        # password field from this form.
        form_class = super(UserAdmin, self).scaffold_form()

        # Add a password field, naming it "password2" and labeling it "New Password".
        form_class.password2 = PasswordField('New Password')
        return form_class

    # This callback executes when the user saves changes to a newly-created or edited User -- before the changes are
    # committed to the database.
    def on_model_change(self, form, model, is_created):

        # If the password field isn't blank...
        if len(model.password2):

            # ... then encrypt the new password prior to storing it in the database. If the password field is blank,
            # the existing password in the database will be retained.
            model.password = utils.encrypt_password(model.password2)


# Customized Role model for SQL-Admin
class RoleAdmin(sqla.ModelView):

    # Prevent administration of Roles unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')

class ServerView(sqla.ModelView):

    # require user role.
    def is_accessible(self):
        return current_user.has_role('user')

    def _handle_view(self, name,**kwargs):
        if current_user.has_role('admin'):
            self.can_delete = True
        else:
            self.can_delete = False

    def _notes_formatter(view, context, model, name):
        return Markup("%s" % (model.notes)) if model.notes else ""
    def _storage_formatter(view, context, model, name):
        return Markup("%s" % (model.storage)) if model.storage else ""

    # example of default filter for list.
    #~ def get_query(self):
        #~ return self.session.query(self.model).filter(self.model.active == True)

    page_size = 10
    can_view_details = True
    create_modal = True
    edit_modal = True
    details_modal = True
    can_export = True

    column_searchable_list = ['name','full_name','storage','notes',]
    column_filters = ['name', 'full_name', 'cpu_cores', 'memory', 'compute_units', 'virtual', 'creator.username',
                      'creator.name', 'creator.email','storage','notes','version', 'active',]   # example custom filter: FilterActiveServer(column=Server.active, name='Only Active', options=((True, 'Yes'), (False, 'No')))]
    column_editable_list = ['name', 'full_name', 'cpu_cores', 'memory', 'compute_units', 'virtual', 'storage', 'notes','version','active']
    column_list = ['name','full_name','version','active','cpu_cores', 'compute_units', 'memory', 'virtual', 'storage', 'notes', 'creator',]
    column_exclude_list = ['storage']
    column_labels = dict(cpu_cores='CPU Cores')
    # sort by name, descending
    column_default_sort = ('name', False)

    form_excluded_columns = ('creator_id')

    column_formatters = {
        'storage': _storage_formatter,
        'notes': _notes_formatter,
    }

    form_args = {
        'cpu_cores': {
            'label': 'CPU Cores'
        },
        'memory': {
            'label': 'Memory (gb)'
        },
    }

    form_widget_args = {
        'name': {
            'placeholder': 'server short name',
        },
        'full_name': {
            'placeholder': 'server full name',
        },
        'cpu_cores': {
            #'style': 'width: 50px',
            'placeholder': 'number of cores',
            'title': 'total number of cpu cores in server\n2 cpus with 2 cores each = 4 cores',
        },
        'version': {
            'placeholder': 'version of server',
            'title': 'version of server (used to distinguish hw upgrades - e.g. rebuilt as larger ec2 instance)',
        },
        'active': {
            'title': 'is the server active (used to deactivate old/unavailable instances of a server)',
        },
        'memory': {
            #'style': 'width: 77px',
            'placeholder': 'amount of memory',
            'title': 'amount of memory (in gb) in server',
        },
        'compute_units': {
            #'style': 'width: 77px',
            'placeholder': 'amount of guaranteed compute units',
            'title': 'amount of guaranteed compute units for server (e.g. the ECU # for EC2 instances)\nnote: leave blank if unknown or variable',
        },
        'virtual': {
            'style': 'width: 25px',
            'title': 'is this server virtual or physical?',
        },
        'storage': {
            'placeholder': 'storage type and size for all disks',
            'title': 'storage type (hdd, ssd, etc.) and size for each disk available to server\nnote: please note the date of any changes for this field',
        },
        'notes': {
            'placeholder': 'notes regarding server',
        }
    }

    def on_model_change(self, form, model, is_created):

        if is_created:
            model.creator_id = current_user.id


class TestPlanView(sqla.ModelView):

    # require user role.
    def is_accessible(self):
        return current_user.has_role('user')

    def _handle_view(self, name,**kwargs):
        if current_user.has_role('admin'):
            self.can_delete = True
        else:
            self.can_delete = False

    def _summary_formatter(view, context, model, name):
        return Markup("%s" % (model.summary)) if model.summary else ""
    def _description_formatter(view, context, model, name):
        return Markup("%s" % (model.description)) if model.description else ""
    def _run_info_formatter(view, context, model, name):
        return Markup("%s" % (model.run_info)) if model.run_info else ""
    def _dependencies_formatter(view, context, model, name):
        return Markup("%s" % (model.dependencies)) if model.dependencies else ""
    def _notes_formatter(view, context, model, name):
        return Markup("%s" % (model.notes)) if model.notes else ""

    can_view_details = True
    create_modal = True
    edit_modal = True
    details_modal = True
    can_export = True
    page_size = 10

    column_searchable_list = ['name', 'summary', 'description', 'run_info', 'dependencies', 'notes',]
    column_filters = ['name', 'version', 'source_url', 'summary', 'description', 'run_info', 'dependencies', 'notes',]
    column_editable_list = ['name', 'version', 'source_url', 'summary', 'description', 'run_info', 'notes',]
    column_list = ['name', 'version', 'source_url', 'summary', 'description', 'run_info', 'dependencies', 'notes', 'creator']
    column_exclude_list = ['description', 'run_info', 'dependencies', 'notes']
    column_labels = dict(source_url='Source')
    # sort by name, descending
    column_default_sort = ('name', False)

    form_excluded_columns = ('creator_id')

    column_formatters = {
        'summary': _summary_formatter,
        'description': _description_formatter,
        'run_info': _run_info_formatter,
        'dependencies': _dependencies_formatter,
        'notes': _notes_formatter,
    }

    form_args = {
        'source_url': {
            'label': 'Source'
        },
    }

    form_widget_args = {
        'name': {
            'placeholder': 'test plan name',
        },
        'version': {
            #'style': 'width: 50px',
            'placeholder': 'version',
            'title': 'test script version (e.g. 1.0.0, 1.0.1, etc.)',
        },
        'source_url': {
            #'style': 'width: 77px',
            'placeholder': 'url to source of test script',
            'title': 'url to version control (or other) location of test script',
        },
        'summary': {
            #'style': 'width: 77px',
            'placeholder': 'brief summary of test script',
            'title': 'a brief summary of the test script',
        },
        'description': {
            #'style': 'width: 25px',
            'placeholder': 'detailed description of test script',
            'title': 'a detailed description of the test script',
        },
        'run_info': {
            'placeholder': 'info needed to run the script',
            'title': 'all info needed to run the script such as variables or properties that need to be set',
        },
        'dependencies': {
            'placeholder': 'dependencies of the script',
            'title': 'all dependencies of the script (e.g. fakeusers.csv,  or other files, apps, data, info, etc.)',
        },
        'notes': {
            'placeholder': 'notes regarding test script',
            'title': 'any notes or additional detail about the test script',
        }
    }

    def on_model_change(self, form, model, is_created):

        if is_created:
            model.creator_id = current_user.id


class TestResultView(sqla.ModelView):
    @expose('/tya/')
    def index(self):
        return self.render('help-about.html')

    def is_accessible(self):
        return current_user.has_role('user')

    def _handle_view(self, name,**kwargs):
        if current_user.has_role('admin'):
            self.can_delete = True
        else:
            self.can_delete = False

    #~ def _target_server_formatter(view, context, model, name):
        #~ return Markup("<a href='%s'>%s</a>" % (url_for('server.edit_view', id=model.target_server.id), model.target_server.name)) if model.target_server else ""
    #~ def _source_servers_formatter(view, context, model, name):
        #~ return "%s" % (model.source_servers.server) if model.source_servers else ""
    #~ def _test_plan_formatter(view, context, model, name):
        #~ return Markup("<a href='%s'>%s</a>" % (url_for('test_plan.edit_view', id=model.test_plan.id), model.test_plan.name)) if model.test_plan else ""
    def _test_notes_formatter(view, context, model, name):
        return Markup("%s" % (model.test_notes)) if model.test_notes else ""

    #~ def on_form_prefill(self, form, id):
        #~ form.run_by = 'admin'
        #form.process()


    # example to add extra row_actions
    #~ column_extra_row_actions = [
        #~ LinkRowAction('glyphicon glyphicon-off', 'http://direct.link/?id={row_id}'),
        #~ LinkRowAction('glyphicon glyphicon-off', 'tya/?id={row_id}'),
        #~ #EndpointLinkRowAction('glyphicon glyphicon-on', 'testresult.index_view'),
    #~ ]

    page_size = 10
    can_set_page_size = True
    can_view_details = True
    create_modal = True
    edit_modal = True
    details_modal = True
    can_export = True

    column_searchable_list = ['test_plan.name', 'test_notes']
    column_filters = ['test_plan.name', 'test_date', 'number_users', 'run_length', 'number_failures', 'average_response_time',
                      'target_server.name','run_by.name', 'test_passed', 'loop_amount',]
    column_editable_list = ['target_server_id', 'test_date', 'test_plan', 'number_users', 'run_length',
                            'number_failures', 'average_response_time', 'test_passed', 'target_server_cpu', 'target_server_memory',
                            'target_server_load', 'source_servers', 'target_server']
    column_list = ['test_passed', 'test_date', 'test_plan', 'source_servers', 'target_server', 'number_users',
                   'run_length', 'number_failures', 'number_requests', 'average_response_time', 'target_server_cpu',
                   'target_server_memory', 'target_server_load', 'test_notes', 'creator', 'run_by', 'app_version', 'ramp_up',
                   'loop_amount',]
    column_exclude_list = ['run_by', 'loop_amount', 'app_version', 'ramp_up', 'number_requests', 'test_notes', 'creator']
    column_labels = dict(target_server='Target', number_users='#Users', number_failures='#Fail', average_response_time='ART',
                         source_servers='Source', target_server_memory='Mem', target_server_load='Load', target_server_cpu='CPU',
                         test_passed='Pass', loop_amount='Loops',run_length='RunLen',
                         )
    form_excluded_columns = ('created_at','creator_id', 'creator')
    # sort by test_date, descending
    column_default_sort = ('test_date', True)
    #column_default_sort = 'test_plan.name'

    #column_formatters = dict(target_server='target_server.name')
    column_formatters = {
        #'test_plan': _test_plan_formatter,
        #'target_server': _target_server_formatter,
        'test_notes': _test_notes_formatter,
    }

    form_args = {
        'target_server': {
            # filter to only show 'active' servers
            'query_factory': lambda: Server.query.filter_by(active=True)
        },
        'test_passed': {
            'label': 'Pass'
        },
        'loop_amount': {
            'label': 'Loops'
        },
        'number_users': {
            'label': '# Users'
        },
        'number_failures': {
            'label': '# Fail'
        },
        'number_requests': {
            'label': '# Reqs'
        },
        'run_length': {
            'label': 'Run Length'
        },
        'average_response_time': {
            'label': 'ART'
        },
        'target_server_cpu': {
            'label': 'CPU'
        },
        'target_server_memory': {
            'label': 'Memory'
        },
        'target_server_load': {
            'label': 'Load'
        },
    }

    form_widget_args = {
        'test_date': {
            'placeholder': 'date/time test was started',
        },
        #~ 'test_plan': {
            #~ 'placeholder': 'name of test plan executed',
        #~ },
        'loop_amount': {
            'placeholder': '# of loops',
            'title': 'number of loops of the test performed (-1 indicates loop forever)',
        },
        'app_version': {
            'placeholder': 'version of application',
        },
        'number_users': {
            'placeholder': 'number of users ran for test',
        },
        'test_passed': {
            'title': 'did the test run successfully? (Yes|No)',
        },
        'ramp_up': {
            'placeholder': 'ramp up time (in seconds)',
            'title': 'the number of time used to spin up all instances of test users',
        },
        'run_length': {
            'placeholder': 'run length (in seconds)',
            'title': 'how long it took to run the test (in seconds)',
        },
        'number_failures': {
            'placeholder': '# of failures',
            'title': 'number of failures that occurred during the test',
        },
        'number_requests': {
            'placeholder': '# of requests',
            'title': 'number of requests generated during the test',
        },
        'average_response_time': {
            'placeholder': 'average response time (in milliseconds)',
            'title': 'average response time (in milliseconds)',
        },
        'target_server_cpu': {
            'placeholder': 'peak cpu utilization on Target Server',
            'title': 'peak cpu utilization measured on Target Server during test',
        },
        'target_server_memory': {
            'placeholder': 'lowest free memory (in gb) on Target Server',
            'title': 'lowest free memory (in gb) measured on Target Server during test',
        },
        'target_server_load': {
            'placeholder': 'peak server load on Target Server',
            'title': 'peak server load measured on Target Server during test\nnote: this is the 1 minute load of top on target server',
        },
        'run_by': {
            'placeholder': 'who the test was run by',
            'title': 'who ran the test',
        }
    }

    def on_model_change(self, form, model, is_created):

        if is_created:
            model.creator_id = current_user.id
