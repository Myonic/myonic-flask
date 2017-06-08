from flask import request, g, redirect, url_for, render_template, flash, abort
from flask_login import login_required, logout_user
from datetime import datetime as dt
from myonic import app, login_manager
from myonic.models import *
from myonic.blog import *
from myonic.seo import *
from myonic.forms import *

# NOTE: When sending a post object to a template, send it as the variable "post" otherwise THINGS WILL BREAK!

# NOTE: Trail ALL ROUTES with a '/' or the route will not load with a trailing '/' (but it does load without one either way)

@app.route('/')
def index():
    return render_template('layout.html.j2', seo=pageSEO(title='test'))

@app.route('/admin/')
@login_required
def admin():
    return render_template('admin/home.html.j2')

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You have logged out')
    return redirect(url_for('index'))

@app.route('/login/')
def login():
    return render_template('login.html.j2')

# --- Blog System ---

# TODO: Move Blog System routes to blog.py to make app more modular

@app.route('/admin/blogs/', methods = ['GET', 'POST']) # List blogs
@login_required
def listBlogs():
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please enter the name of your new blog')
        else:
            name = request.form['name']
            newBlog(name)

    blogs = getBlogs()
    return render_template('admin/blogs.html.j2', blogs=blogs)

@app.route('/admin/blogs/<blog>/delete/')
@login_required
def deleteBlog(blog):
    deleteaBlog(blog)
    return redirect(url_for('listBlogs'))

@app.route('/admin/blogs/<blog>/') # List posts
@login_required
def blog(blog):
    if getPosts(blog):
        posts = getPosts(blog)
        return render_template('admin/blog.html.j2', blog=blog, posts=posts)
    else:
        return abort(404) # TODO: Add custom 404 eventually

@app.route('/admin/blogs/<blog>/new/', methods = ['GET', 'POST'])
@login_required
def newPost(blog):
    form = editPostForm()
    if form.validate_on_submit():
        createaPost(form, blog)
        return redirect(url_for('blog', blog=blog))
    return render_template('admin/newpost.html.j2', form=form, blog=blog, now=dt.utcnow())

@app.route('/admin/blogs/<blog>/edit/<post>/', methods = ['GET', 'POST'])
@login_required
def editPost(blog, post):
    form = editPostForm()
    if form.validate_on_submit():
        editaPost(form, blog, post)
        return redirect(url_for('blog', blog=blog))
    if BlogPosts.query.filter_by(title=post).all():
        _post = BlogPosts.query.filter_by(title=post).first()
        return render_template('admin/editpost.html.j2', form=form, blog=blog, post=_post)
    else:
        abort(404) # TODO: Add custom 404 eventually

@app.route('/<blog>/<post>/preview/', methods = ['GET', 'POST'])
@login_required
def editPostContent(blog, post):
    if BlogPosts.query.filter_by(title=post).all():
        _post = BlogPosts.query.filter_by(title=post).first()
        return render_template('admin/editpostcontent.html.j2', blog=blog, post=_post)
    else:
        abort(404) # TODO: Add custom 404 eventually

@app.route('/admin/ajax/save', methods=['POST'])
@login_required
def savePostContent():
    print request.form['regions']
    return redirect(url_for('admin'))

@app.route('/admin/blogs/<blog>/<post>/delete/')
@login_required
def deletePost(blog, post):
    deleteaPost(post)
    return redirect(url_for('blog', blog=blog))

#TODO: Error handlers

# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page_not_found.html.j2'), 404
