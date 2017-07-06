from flask import request, g, redirect, url_for, render_template, flash, abort, jsonify
from flask_login import login_required, logout_user, current_user
from datetime import datetime
from time import time
from os.path import join
from slugify import slugify
from PIL import Image
from myonic import app, login_manager
from myonic.models import *
from myonic.seo import *
from myonic.forms import *

# NOTE: When creating page list, sort by route

# NOTE: Change active system to use variables within the templates instead of being passed by the return

# TODO: Change delete and navbar up/down to use forms instead of routes maybe?

@app.before_first_request
def createHomepage():
    if not Pages.query.filter_by(path='').first():
        page = Pages(
        published=True,
        title='Home',
        path='',
        )
        db.session.add(page)
        db.session.commit()
        app.logger.warning('Detected no homepage. This is probably a first run. Homepage created.')
    # if not Site.query.all():
    #     name        = Site(setting='name', data='Site')
    #     short_name  = Site(setting='short_name', data='Site')
    #     twitter     = Site(setting='twitter', data='Site')
    #     facebook    = Site(setting='facebook', data='Site')
    #     email       = Site(setting='name', data='Site')
    #     phone       = Site(setting='name', data='Site')
    #     owner       = Site(setting='name', data='Site')
    #     domain      = Site(setting='name', data='Site')
    #     description = Site(setting='name', data='Site')
    #     google_client_debug = Site(setting='name', data='Site')
    #     google_secret_debug = Site(setting='name', data='Site')
    #     google_client = Site(setting='name', data='Site')
    #     google_secret = Site(setting='name', data='Site')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config.get('ALLOWED_EXTENSIONS')

@app.route('/admin/')
@login_required
def admin():
    return render_template('admin/admin.html.j2')

@app.route('/admin/pages/')
@login_required
def listPages():
    pages = Pages.query.order_by('path')
    return render_template('admin/allpages.html.j2', pages=pages, active='pages')

@app.route('/admin/pages/new/', methods=['GET', 'POST'])
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
        flash('You created the page %s! It is not published yet.' % form.title.data, category='success')
        return redirect(url_for('page', path=form.path.data[1:]))
    else:
        return render_template('admin/createpage.html.j2', form=form, active='pages')

@app.route('/admin/page/delete/<int:id>/confirm/', methods=['GET', 'POST'])
@login_required
def deletePage(id):
    page = Pages.query.filter_by(id=id).first()
    db.session.delete(page)
    db.session.commit()
    flash('Deleted the page <b>%s</b>' % page.title, category='success')
    return redirect(url_for('listPages'))

@app.route('/admin/blog/')
@login_required
def blogSettings():
    return render_template('admin/blogsettings.html.j2', active='blog')

@app.route('/admin/blog/posts/')
@login_required
def listPosts():
    posts = Posts.query.order_by(Posts.datePublished.desc())
    return render_template('admin/allposts.html.j2', posts=posts, active='blog')

@app.route('/admin/blog/posts/new/', methods=['GET', 'POST'])
@login_required
def newPost():
    form = createPostForm()
    if Categories.query.all():
        form.category.choices = [(category.id, category.name) for category in Categories.query.order_by('name')]
    else:
        form.category.choices = [(0, '(No Categories)')]
        flash('<b>Your blog has no categories.</b> Some things may not work if you don\'t have a category assigned. <a href="%s" class="alert-link">You may want to add one before creating a post.</a>' % url_for('categories'), category='warning')
    if form.validate_on_submit():
        if form.category.data == 0:
            category = None
        else:
            category = form.category.data
        if form.tags.data:
            tags = [(tag.lower()) for tag in form.tags.data.lower().split(', ')]
        else:
            tags = None
        # Upload file
        file = form.image.data
        fname = ''
        if file:
            ext = file.filename.rsplit('.', 1)[1]
            fname = str(int(time() * 1000)) + '.' + ext
            file.save(join(app.config.get('UPLOAD_FOLDER'), fname))
        else:
            flash('The image upload failed because the file was missing', category='danger')
        post = Posts(
        published=False,
        title=form.title.data,
        slug=slugify(form.title.data),
        description=form.description.data,
        category=category,
        tags=tags,
        datePublished=form.date.data,
        author=current_user.email,
        image= 'uploads/' + fname
        )
        db.session.add(post)
        db.session.commit()
        flash('You created the post <b>%s</b>! It is not published yet.' % form.title.data, category='success')
        return redirect(url_for('listPosts')) # TODO: Fix redirect
    else:
        return render_template('admin/createpost.html.j2', form=form, active='blog')

@app.route('/admin/blog/posts/edit/<int:id>/', methods=['GET', 'POST'])
@login_required
def editPost(id):
    form = editPostForm()
    post = Posts.query.filter_by(id=id).first()
    form.author.choices = [(user.id, user.first_name + ' ' + user.last_name) for user in Users.query.order_by('first_name')]
    if Categories.query.all():
        form.category.choices = [(category.id, category.name) for category in Categories.query.order_by('name')]
    else:
        form.category.choices = [(0, '(No Categories)')]
        flash('<b>Your blog has no categories.</b> Some things may not work if you don\'t have a category assigned. <a href="%s" class="alert-link">You may want to add one before creating a post.</a>' % url_for('categories'), category='warning')
    if form.validate_on_submit():
        if form.category.data == 0:
            category = None
        else:
            category = form.category.data
        if form.tags.data:
            tags = [(tag.lower()) for tag in form.tags.data.lower().split(', ')]
        else:
            tags = None
        # Upload file
        file = form.image.data
        fname = ''
        if file:
            ext = file.filename.rsplit('.', 1)[1]
            fname = str(int(time() * 1000)) + '.' + ext
            file.save(join(app.config.get('UPLOAD_FOLDER'), fname))
            post.image= 'uploads/' + fname
        post.slug=slugify(form.slug.data)
        post.description=form.description.data
        post.category=category
        post.tags=tags
        post.datePublished=form.date.data
        post.author=Users.query.filter_by(id=form.author.data).first().email
        db.session.add(post)
        db.session.commit()
        flash('Successfully edited the post <b>%s</b>.' % post.title, category='success')
        return redirect(url_for('listPosts')) # TODO: Fix redirect
    else:
        return render_template('admin/postsettings.html.j2', form=form, post=post, active='blog')

@app.route('/admin/post/delete/<int:id>/confirm/', methods=['GET', 'POST'])
@login_required
def deletePost(id):
    post = Posts.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    flash('Deleted the post <b>%s</b>' % post.title, category='success')
    return redirect(url_for('listPosts'))

@app.route('/admin/blog/categories/', methods=['GET', 'POST'])
@login_required
def categories():
    form = createCategoryForm()
    categories = Categories.query.order_by('name')
    if form.validate_on_submit():
        category = Categories(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('You created the category <b>%s</b>!' % form.name.data, category='success')
    return render_template('admin/categories.html.j2', form=form, categories=categories, active='blog')

@app.route('/admin/blog/categories/edit/<int:id>/', methods=['GET', 'POST'])
@login_required
def editCategory(id):
    form = createCategoryForm()
    category = Categories.query.filter_by(id=id).first()
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.add(category)
        db.session.commit()
        flash('The category <b>%s</b> was updated!' % form.name.data, category='success')
        return redirect(url_for('categories'))
    return render_template('admin/updatecategory.html.j2', form=form, category=category, active='blog')

@app.route('/admin/category/delete/<int:id>/confirm/', methods=['GET', 'POST'])
@login_required
def deleteCategory(id):
    category = Categories.query.filter_by(id=id).first()
    db.session.delete(category)
    db.session.commit()
    flash('Deleted the category <b>%s</b>' % category.name, category='success')
    return redirect(url_for('categories'))

@app.route('/admin/me/')
@login_required
def userSettings():
    pass

@app.route('/admin/settings/')
@login_required
def siteSettings():
    return render_template('admin/sitesettings.html.j2', active='settings')

# TODO: Limit items
@app.route('/admin/settings/navbar/', methods=['GET', 'POST'])
@login_required
def navbarSettings():
    urlform = addURLNavitemForm()
    pageform = addPageNavitemForm()
    pageform.page.choices = [(page.id, page.title + ': ' + (page.path if page.path != '' else '/')) for page in Pages.query.order_by('title')]
    if request.args.get('form') == 'urlform':
        if urlform.validate_on_submit():
            if Navbar.query.all():
                index = Navbar.query.order_by(Navbar.index.desc()).first().index + 1
            else:
                index = 1
            item = Navbar(
            index = index,
            label = urlform.label.data,
            type = 'url',
            url = urlform.url.data
            )
            db.session.add(item)
            db.session.commit()
            flash('Item Added!', category='success')
    if request.args.get('form') == 'pageform':
        if pageform.validate_on_submit():
            if Navbar.query.all():
                index = Navbar.query.order_by(Navbar.index.desc()).first().index + 1
            else:
                index = 1
            item = Navbar(
            index = index,
            label = pageform.label.data,
            type = 'page',
            page = pageform.page.data
            )
            db.session.add(item)
            db.session.commit()
            flash('Item Added!', category='success')
    navitems = Navbar.query.order_by('index').all()
    return render_template('admin/navbarsettings.html.j2', navitems=navitems, urlform=urlform, pageform=pageform, active='settings')

@app.route('/admin/settings/navbar/down/<int:index>/')
@login_required
def navbarDown(index):
    if Navbar.query.filter_by(index=index + 1).all():
        swap = Navbar.query.filter_by(index=index + 1).first()
    else:
        app.logger.warning('nop')
        return redirect(url_for('navbarSettings'))
    navitem = Navbar.query.filter_by(index=index).first()
    navitem.index += 1
    swap.index -= 1
    db.session.add(navitem, swap)
    db.session.commit()
    return redirect(url_for('navbarSettings'))

@app.route('/admin/settings/navbar/up/<int:index>/')
@login_required
def navbarUp(index):
    if Navbar.query.filter_by(index=index - 1).all():
        swap = Navbar.query.filter_by(index=index - 1).first()
    else:
        app.logger.warning('nop')
        return redirect(url_for('navbarSettings'))
    navitem = Navbar.query.filter_by(index=index).first()
    navitem.index -= 1
    swap.index += 1
    db.session.add(navitem, swap)
    db.session.commit()
    return redirect(url_for('navbarSettings'))

@app.route('/admin/settings/navbar/delete/<int:id>/')
@login_required
def navbarDelete(id):
    navbar = Navbar.query.all()
    navitem = Navbar.query.filter_by(id=id).first()
    for item in navbar:
        if item.index > navitem.index:
            item.index -= 1
            db.session.add(item)
    db.session.delete(navitem)
    db.session.commit()
    return redirect(url_for('navbarSettings'))

@app.route('/admin/logout/')
@login_required
def logout():
    logout_user()
    flash('You have logged out', category='info')
    return redirect(url_for('page', path=''))

@app.route('/admin/login/')
def login():
    if current_user.is_authenticated:
        flash('You are already logged in', category='warning')
        return redirect(url_for('page', path=''))
    else:
        return redirect(url_for('google.login'))

@app.route('/admin/ajax/page/save', methods=['POST'])
@login_required
def savePageContent():
    data = json.loads(request.form['regions'])
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

@app.route('/admin/ajax/post/save', methods=['POST'])
@login_required
def savePostContent():
    data = json.loads(request.form['regions'])
    if Posts.query.filter_by(id=request.form['post_id']).all():
        post = Posts.query.filter_by(id=request.form['post_id']).first()
        try:
            if data['title']:
                post.title = str(data['title'])
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
    return jsonify({'size' : file.size, 'url' : url_for('static', filename='uploads/' + fname)}) # TODO: Does not take into account the UPLOAD_FOLDER configuration when returning the image. Maybe instead, remove it as a configurable option and just make the location static.

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
    nav = Navbar.query.order_by('index').all()
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
        return render_template('home.html.j2', page=page, form=form, nav=nav, seo=pageSEO(title=page.title, description=page.description))
    elif Pages.query.filter_by(path=path).all():
        page = Pages.query.filter_by(path=path).first()
        if page.published:
            return render_template('page.html.j2', page=page, form=form, nav=nav, seo=pageSEO(title=page.title, description=page.description))
        elif current_user.is_authenticated:
            return render_template('page.html.j2', page=page, form=form, nav=nav, seo=pageSEO(title=page.title, description=page.description))
        else:
            abort(404)
    else:
        abort(404)

@app.route('/', defaults={'slug': ''}, subdomain='blog')
@app.route('/<path:slug>/', subdomain='blog')
@app.route('/blog/', defaults={'slug': ''}, endpoint='blog-canonical', methods=['GET', 'POST']) # TODO: Make part of Admin blueprint
@app.route('/blog/<path:slug>/', endpoint='blog-canonical', methods=['GET', 'POST']) # TODO: Make part of Admin blueprint
def blog(slug):
    nav = Navbar.query.order_by('index').all()
    # TODO: Allow site to run blog system on timezone other then UTC
    if current_user.is_authenticated:
        form = editPostFormInpage()
        if request.method == 'POST':
            if form.validate_on_submit():
                post = Posts.query.filter_by(slug=slug).first()
                post.description = form.description.data
                post.slug = slugify(form.slug.data)
                post.published = form.published.data
                db.session.add(post)
                db.session.commit()
                return redirect(url_for('blog-canonical', slug=slugify(form.slug.data)))
    else:
        form = None

    if slug == '':
        posts=Posts.query.filter(Posts.datePublished <= datetime.date.today(), Posts.published).order_by(Posts.datePublished.desc()).limit(5)
        return render_template('postlist.html.j2', posts=posts, nav=nav, seo=pageSEO(title='Blog', type='blog'))
    elif Posts.query.filter_by(slug=slug).all():
        post = Posts.query.filter_by(slug=slug).first()
        if post.published and post.datePublished <= datetime.date.today():
            return render_template('post.html.j2', post=post, form=form, nav=nav, seo=articleSEO(title=post.title, postDate=post.datePublished, author=post.users.first_name + ' ' + post.users.last_name, category=post.categories.name, twitter_type='summery', description=post.description)) # TODO: Define twitter_type based on if featured image is present or not
        elif current_user.is_authenticated:
            if post.published and post.datePublished >= datetime.date.today():
                flash('Post is set currently set to publish on %s. Flipping the publish switch to off will prevent it from posting automatically.' % post.datePublished.strftime('%m/%d/%Y'))
            return render_template('post.html.j2', post=post, form=form, nav=nav, seo=articleSEO(title=post.title, postDate=post.datePublished, author=post.users.first_name + ' ' + post.users.last_name, category=post.categories.name, twitter_type='summery', description=post.description)) # TODO: Define twitter_type based on if featured image is present or not
        else:
            abort(404)
    else:
        abort(404)

#TODO: Error handlers

# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page_not_found.html.j2'), 404
