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

app.config['SECRET_KEY'] = 'myopotskavynomaj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myonic.sqlite3'









if __name__ == '__main__':
    app.run()
