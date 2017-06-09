from flask import request, g, redirect, url_for, render_template, flash, abort, jsonify
from flask_login import login_required, logout_user
from datetime import datetime as dt
from time import time
from os.path import join
from PIL import Image
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
    if BlogPosts.query.filter_by(slug=post).all():
        _post = BlogPosts.query.filter_by(slug=post).first()
        return render_template('admin/editpost.html.j2', form=form, blog=blog, post=_post)
    else:
        abort(404) # TODO: Add custom 404 eventually

@app.route('/<blog>/<post>/preview/', methods = ['GET', 'POST'])
@login_required
def editPostContent(blog, post):
    if BlogPosts.query.filter_by(slug=post).all():
        post = BlogPosts.query.filter_by(slug=post).first()
        return render_template('admin/editpostcontent.html.j2', blog=blog, post=post)
    else:
        abort(404) # TODO: Add custom 404 eventually

@app.route('/admin/ajax/save', methods=['POST'])
@login_required
def savePostContent():
    data = json.loads(request.form['regions'])
    print('pinged')
    if BlogPosts.query.filter_by(id=request.form['post_id']).all():
        post = BlogPosts.query.filter_by(id=request.form['post_id']).first()
        try:
            if data['title']:
                post.title = str(data['title'])
                post.slug = str(data['title'].lower().replace(' ', '-'))
        except KeyError:
            pass
        try:
            if data['content']:
                post.content = str(data['content'])
        except KeyError:
            pass
        db.session.add(post)
        db.session.commit()
    return "ok"

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config.get('ALLOWED_EXTENSIONS')

@app.route('/admin/ajax/image/upload', methods=['POST'])
@login_required
def uploadImageFromEditor():
    file = request.files['image']
    fname = ''
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1]
        fname = str(int(time() * 1000)) + '.' + ext
        file.save(join(app.config.get('UPLOAD_FOLDER'), fname))
    file = Image.open(join(app.config.get('UPLOAD_FOLDER'), fname))
    return jsonify({'size' : file.size, 'url' : url_for('static', filename='uploads/' + fname)})

@app.route('/admin/ajax/image/rotate', methods=['POST'])
@login_required
def rotateImageFromEditor():
    fname = request.form['url'].split('/')[-1].split('#')[0].split('?')[0]
    file = Image.open(join(app.config.get('UPLOAD_FOLDER'), fname))
    if request.form['direction'] == 'CW':
        file.rotate(90).save(join(app.config.get('UPLOAD_FOLDER'), fname))
    else:
        file.rotate(-90).save(join(app.config.get('UPLOAD_FOLDER'), fname))
    file = Image.open(join(app.config.get('UPLOAD_FOLDER'), fname))
    return jsonify({'size' : file.size, 'url' : url_for('static', filename='uploads/' + fname)})

@app.route('/admin/ajax/image/insert', methods=['POST'])
@login_required
def insertImageFromEditor():
    fname = request.form['url'].split('/')[-1].split('#')[0].split('?')[0]
    file = Image.open(join(app.config.get('UPLOAD_FOLDER'), fname))
    width = file.size[0]
    height = file.size[1]
    crop = request.form['crop'].split(",")
    file = file.crop((
        int(width * float(crop[1])),
        int(height * float(crop[0])),
        int(width * float(crop[3])),
        int(height * float(crop[2]))
    ))
    file.save(join(app.config.get('UPLOAD_FOLDER'), 'c' + fname))
    # Crop, save as new file, and then do something
    # print request.form
    return jsonify({'size' : file.size, 'url' : url_for('static', filename='uploads/' + 'c' + fname)})

@app.route('/admin/blogs/<blog>/<post>/delete/')
@login_required
def deletePost(blog, post):
    deleteaPost(post)
    return redirect(url_for('blog', blog=blog))

#TODO: Error handlers

# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page_not_found.html.j2'), 404
