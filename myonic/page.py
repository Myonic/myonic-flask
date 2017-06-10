from flask import  Flask, abort, flash, redirect, render_template, request, url_for, request, Response
from myonic import app
from myonic.models import *

# def getBlogs():
#     blogs = Blogs.query.all()
#     return blogs

# def newBlog(name):
#     if not Blogs.query.filter_by(name=name).all():
#         newblog = Blogs(name=name, slug=name.lower().replace(' ','-'))
#         db.session.add(newblog)
#         db.session.commit()
#         flash('You created the blog %s!' % name)
#     else:
#         flash('A blog with that name already exsists')

# def deleteaBlog(blog):
#     Blogs.query.filter_by(slug=blog).delete()
#     db.session.commit()
#     flash('You deleted "%s". If you want to restore this blog, just type the name and all the posts reappear.' % blog)

# def getPosts(blog):
#     if Blogs.query.filter_by(slug=blog).all():
#         blog_id = Blogs.query.filter_by(slug=blog).first()
#         posts = Pages.query.filter_by(blog=blog_id.id)
#         return posts

def createPage(form):
    page = Pages(
    published=False,
    title=form.title.data,
    path=form.slug.data,
    description=form.description.data,
    )
    db.session.add(page)
    db.session.commit()
    flash('You created the page %s! This page is not yet published. Click the post to edit it\'s data and content.' % form.title.data)

def editPage(form):
    post = Pages.query.filter_by(path=post).first()
    post.published=form.published.data
    post.title=form.title.data
    post.description=form.description.data
    post.path=form.path.data,
    db.session.add(post)
    db.session.commit()
    flash('Edited settings for %s' % form.title.data)

def deletePage(post):
    Pages.query.filter_by(path=post).delete()
    db.session.commit()
    flash('You deleted "%s".' % post)
