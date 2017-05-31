from flask import Flask
from flask_login import LoginManager

from flask_assets import Environment, Bundle

# TODO: File logs of errors and user activity

app = Flask(__name__)

assets = Environment(app)

bundles = {
    # SASS compile
    'sass': Bundle(
    '*.sass',
    filters='sass',
    output='gen/sass'
    )
}

assets.register(bundles)

app.config.from_pyfile('configs.py')

login_manager = LoginManager()
login_manager.login_view = 'google.login'

from userauth import *
from routes import *

login_manager.init_app(app)

db.create_all()
db.session.commit()
