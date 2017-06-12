from flask import request, g, redirect, url_for, render_template, flash, abort, jsonify
from flask_login import login_required, logout_user, current_user
from datetime import datetime as dt
from time import time
from os.path import join
from PIL import Image
from myonic import app, login_manager
from myonic.models import *
from myonic.seo import *
from myonic.forms import *

# NOTE: When creating page list, sort by route

@app.before_first_request
def createHomepage():
    if not Pages.query.filter_by(path='').first():
        page = Pages(
        published=True,
        title='Homepage',
        path='',
        )
        db.session.add(page)
        db.session.commit()
        print('Detected no homepage. This is probably a first run. Homepage created.')

@app.route('/admin/new/', methods=['GET', 'POST'])
@login_required
def newPage():
    form = createPageForm()
    if form.validate_on_submit():
        page = Pages(
        published=False,
        title=form.title.data,
        path=form.path.data,
        description=form.description.data
        )
        db.session.add(page)
        db.session.commit()
        flash('You created the page %s! It is not published yet.' % form.title.data)
        return redirect(url_for('page', path=form.path.data[1:]))
    else:
        return render_template('createpage.html.j2', form=form)

@app.route('/admin/logout/')
@login_required
def logout():
    logout_user()
    flash('You have logged out')
    return redirect(url_for('page', path=''))

@app.route('/admin/login/')
def login():
    if current_user.is_authenticated:
        flash('You are already logged in')
        return redirect(url_for('page', path=''))
    else:
        return render_template('login.html.j2')

@app.route('/admin/ajax/save', methods=['POST'])
@login_required
def savePostContent():
    data = json.loads(request.form['regions'])
    print('pinged')
    if Pages.query.filter_by(id=request.form['page_id']).all():
        page = Pages.query.filter_by(id=request.form['page_id']).first()
        try:
            if data['title']:
                page.title = str(data['title'])
        except KeyError:
            pass
        try:
            if data['content']:
                page.content = str(data['content'])
        except KeyError:
            pass
        db.session.add(page)
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

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>/', methods=['GET', 'POST'])
def page(path):
    if current_user.is_authenticated:
        form = editPageForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                path = '/' + path
                page = Pages.query.filter_by(path=path).first()
                page.description = form.description.data
                page.path = form.path.data
                page.published = form.published.data
                db.session.add(page)
                db.session.commit()
                return redirect(url_for('page', path=form.path.data[1:]))
    else:
        form = None

    path = '/' + path

    #TODO: Fix page SEO passthrough

    if path == '/':
        page = Pages.query.filter_by(path='').first()
        return render_template('home.html.j2', page=page, form=form, seo=pageSEO(title='test'))
    elif Pages.query.filter_by(path=path).all():
        page = Pages.query.filter_by(path=path).first()
        if page.published:
            return render_template('page.html.j2', page=page, form=form, seo=pageSEO(title='test'))
        elif current_user.is_authenticated:
            return render_template('page.html.j2', page=page, form=form, seo=pageSEO(title='test'))
        else:
            abort(404)
    else:
        abort(404)

#TODO: Error handlers

# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page_not_found.html.j2'), 404
