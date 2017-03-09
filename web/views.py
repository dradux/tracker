from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from flask.ext.admin import Admin, BaseView, expose, AdminIndexView
from flask.ext.security import current_user, utils
from wtforms import validators
from wtforms.fields import PasswordField

# Customized User model admin
#~ class UserAdmin(sqla.ModelView):
    #~ inline_models = (UserInfo,)


# Customized Post model admin
#~ class PostAdmin(sqla.ModelView):
    #~ # Visible columns in the list view
    #~ column_exclude_list = ['text']

    #~ # List of columns that can be sorted. For 'user' column, use User.username as
    #~ # a column.
    #~ column_sortable_list = ('title', ('user', 'user.username'), 'date')

    #~ # Rename 'title' columns to 'Post Title' in list view
    #~ column_labels = dict(title='Post Title')

    #~ column_searchable_list = ('title', User.username, 'tags.name')

    #~ column_filters = ('user',
                      #~ 'title',
                      #~ 'date',
                      #~ 'tags',
                      #~ filters.FilterLike(Post.title, 'Fixed Title', options=(('test1', 'Test 1'), ('test2', 'Test 2'))))

    #~ # Pass arguments to WTForms. In this case, change label for text field to
    #~ # be 'Big Text' and add required() validator.
    #~ form_args = dict(
                    #~ text=dict(label='Big Text', validators=[validators.required()])
                #~ )

    #~ form_ajax_refs = {
        #~ 'user': {
            #~ 'fields': (User.username, User.email)
        #~ },
        #~ 'tags': {
            #~ 'fields': (Tag.name,)
        #~ }
    #~ }

    #~ def __init__(self, session):
        #~ # Just call parent class with predefined model.
        #~ super(PostAdmin, self).__init__(Post, session)


#~ class TreeView(sqla.ModelView):
    #~ form_excluded_columns = ['children', ]

class HomeView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('home.html')

class HelpView(BaseView):
    @expose('/')
    def index(self):
        return self.render('help.html')

    @expose('/online-help')
    def helpOnline(self):
        return self.render('help.html')

    @expose('/about')
    def helpAbout(self):
        return self.render('about.html')

# Customized User model for SQL-Admin
class UserAdmin(sqla.ModelView):

    # Don't display the password on the list of Users
    column_exclude_list = ('password',)

    # Don't include the standard password field when creating or editing a User (but see below)
    form_excluded_columns = ('password',)

    # Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True

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

    can_delete = False
    page_size = 20

    column_searchable_list = ['name']
    column_editable_list = ['name', 'cpu_cores', 'memory', 'compute_units', 'virtual', 'storage', 'notes']
    column_filters = ['name', 'cpu_cores', 'memory', 'compute_units', 'virtual']

    create_modal = True
    edit_modal = True

    can_export = True

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
            'placeholder': 'server name',
        },
        'cpu_cores': {
            #'style': 'width: 50px',
            'placeholder': 'number of cores',
            'title': 'total number of cpu cores in server\n2 cpus with 2 cores each = 4 cores',
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


class TestResultView(sqla.ModelView):

    def is_accessible(self):
        return current_user.has_role('user')

    can_delete = False
    page_size = 50
    can_view_details = True

    column_exclude_list = ['app_version','ramp_up','number_requests','target_server_cpu','target_server_memory','target_server_load','test_notes',]

    column_searchable_list = ['test_plan']
    column_editable_list = ['source_server_id', 'target_server_id', 'test_date', 'test_plan', 'number_users', 'run_length', 'number_failures', 'average_response_time']
    column_filters = ['test_plan', 'test_date', 'number_users', 'run_length', 'number_failures', 'average_response_time']

    create_modal = True
    edit_modal = True

    can_export = True

    form_args = {
        'number_users': {
            'label': '# Users'
        },
        'number_failures': {
            'label': '# Fail'
        },
        'number_requests': {
            'label': '# Requests'
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
        'test_plan': {
            'placeholder': 'name of test plan executed',
        },
        'app_version': {
            'placeholder': 'version of application',
        },
        'number_users': {
            'placeholder': 'number of users ran for test',
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
    }
