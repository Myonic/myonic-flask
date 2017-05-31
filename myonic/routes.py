from flask import request, g, redirect, url_for, render_template, flash
from flask_login import login_required
from myonic import app, login_manager
from models import *
from seo import getSiteInfo

@app.route('/')
def index():
    return render_template('layout.html', title='test', type='page')

@app.route('/admin')
@login_required
def admin():
    pass

# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page_not_found.html'), 404
