from flask import Flask
from flask_login import LoginManager
from flask_assets import Environment, Bundle
from flask_debugtoolbar import DebugToolbarExtension
import os
# from flask_assets import Environment, Bundle

# TODO: File logs of errors and user activity

# TODO: When email system is added, send welcome email to new users

# TODO: Standardize naming schemes for everything (files, classes, methods, variables)

# TODO: Smart linking on post/page editor for links to other parts of site

app = Flask(__name__)

assets = Environment(app)

# This can later be used to optimize CSS delivery by preventing admin CSS from being delivered if not logged in
bundles = {
    # SASS compile
    'css': Bundle(
        Bundle(
        'content-tools/content-tools.min.css'
        ),
        Bundle(
        'css/style.scss',
        filters='scss,cssmin',
        output='css/style.min.css'
        )
    ),
    'js': Bundle(
    'js/jquery-3.2.1.min.js',
    'js/jquery.stickybits.min.js',
    'js/bootstrap.min.js',
    'js/scrollreveal.min.js',
    ),
    'admin-css': Bundle(
    'css/style-admin.scss',
    filters='scss',
    output='css/style-admin.min.css'
    ),
    'pageadmin-js': Bundle(
    'content-tools/content-tools.min.js',
    'content-tools/pageEditor.js',
    ),
    'postadmin-js': Bundle(
    'content-tools/content-tools.min.js',
    'content-tools/postEditor.js',
    ),
    'admin-js': Bundle(
    'js/jquery-3.2.1.min.js',
    'js/bootstrap.min.js',
    'js/bootstrap-tokenfield.min.js',
    'js/bootstrap-datepicker.min.js'
    )
}

assets.register(bundles)

# NOTE: Jinja Settings not working
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.config.from_pyfile('configs.py')

toolbar = DebugToolbarExtension(app)

login_manager = LoginManager()
login_manager.login_view = 'google.login'

from myonic.userauth import *
from myonic.routes import *

login_manager.init_app(app)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

# Append data to static file names to force client update if file is updated
def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
