from datetime import datetime
import os 
import random
import string
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask import request, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


app = Flask(__name__)


app.config.from_pyfile('configs.py')



db = SQLAlchemy(app)

from configs import *
from util import *

db.create_all()
db.session.commit()



if __name__ == '__main__':
    app.run()
