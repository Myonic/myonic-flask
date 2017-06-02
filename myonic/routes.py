from flask import request, g, redirect, url_for, render_template, flash
from flask_login import login_required, logout_user
from myonic import app, login_manager
from myonic.models import *
from myonic.blog import *
from myonic.seo import *
from myonic.forms import *

# NOTE: When sending a post object to a template, send it as the variable "post" otherwise THINGS WILL BREAK!

@app.route('/')
def index():
    return render_template('layout.html.j2', seo=pageSEO(title='test'))

@app.route('/admin/')
@login_required
def admin():
    return render_template('admin/home.html.j2')

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
def deleteaBlog(blog):
    deleteBlog(blog)
    flash('You deleted' + blog + '. If you want to restore this blog, just type the name and all the posts reappear.')
    return redirect(url_for('listBlogs'))

@app.route('/admin/blogs/<blog>/') # List posts
@login_required
def blog(blog):
    posts = getPosts(blog)
    return render_template('admin/blog.html.j2', blog=blog, posts=posts)

@app.route('/admin/blogs/<blog>/new/', methods = ['GET', 'POST'])
@login_required
def newPost(blog):
    form = editPost()
    if form.validate_on_submit():
        createPost(form, blog)
        return redirect(url_for('blog', blog=blog))
    return render_template('admin/newpost.html.j2', form=form)

@app.route('/admin/blogs/<blog>/<post>/')
@login_required
def editaPost(blog, post):
    pass

@app.route('/admin/blogs/<blog>/<post>/delete')
@login_required
def deletePost(blog, post):
    pass

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You have logged out')
    return redirect(url_for('index'))

@app.route('/login/')
def login():
    return render_template('login.html.j2')

#TODO: Error handler

# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page_not_found.html.j2'), 404
