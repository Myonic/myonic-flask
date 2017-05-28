from flask import request, g, redirect, url_for, render_template, flash
from myonic import app, login_manager
from models import *
from seo import getSiteInfo

@app.route('/')
def index():
    return render_template('layout.html', title='test', type='page')
