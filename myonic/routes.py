from flask import request, g, redirect, url_for, render_template, flash
from flask_login import login_required, logout_user
from myonic import app, login_manager
from myonic.models import *
<<<<<<< Updated upstream
from myonic.seo import getSiteInfo
=======
from seo import getSiteInfo
from myonic.blogs import *
>>>>>>> Stashed changes

@app.route('/')
def index():
    return render_template('layout.html', title='test', type='page')

@app.route('/admin')
@login_required
def admin():
    return render_template('admin/home.html')

@app.route('/admin/blogs', methods = ['GET', 'POST']) # List blogs
def listBlogs():
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please enter the name of your new blog')
        else:
            name = request.form['name']
            newblog(name)
    
    blogs = getblogs()
    return render_template('admin/blogs.html', blogs=blogs)

@app.route('/admin/blogs/<blog>') # List posts
def blog(blog):
    pass

@app.route('/admin/blogs/<blog>/<post>')
def editPost(blog, post):
    pass

@app.route('/admin/blogs/<blog>/post/new')
def newPost(blog):
    pass

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out')
    return redirect(url_for('index'))

@app.route('/login')
def login():
    return render_template('login.html')

# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page_not_found.html'), 404
