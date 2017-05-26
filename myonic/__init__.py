from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from models import db

# TODO: File logs of errors and user activity

app = Flask(__name__)

app.config.from_pyfile('configs.py')

login_manager = LoginManager()
login_manager.login_view = 'google.login'

migrate = Migrate(app, db)

from myonic import userauth

db.init_app(app)
login_manager.init_app(app)
