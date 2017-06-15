from flask import Flask
from flask_login import LoginManager
# from flask_assets import Environment, Bundle

# TODO: File logs of errors and user activity

app = Flask(__name__)

# assets = Environment(app)
#
# bundles = {
#     # SASS compile
#     'sass': Bundle(
#     'css/style.scss',
#     filters='sass',
#     output='gen/style.css'
#     )
# }
#
# assets.register(bundles)
# NOTE: Remove Flask Assets?

app.config.from_pyfile('configs.py')

login_manager = LoginManager()
login_manager.login_view = 'google.login'

from myonic.userauth import *
from myonic.routes import *

login_manager.init_app(app)
