from flask import  Flask, abort, flash, redirect, render_template, request, url_for, request, Response
from myonic import app
from myonic.models import *

def getBlogs():
    blogs = Blogs.query.all()
    return blogs

def newBlog(name):
    if not Blogs.query.filter_by(name=name).all():
        newblog = Blogs(name=name, slug=name.lower().replace(' ','-'))
        db.session.add(newblog)
        db.session.commit()
        flash('You created the blog %s!' % name)
    else:
        flash('A blog with that name already exsists')

def deleteaBlog(blog):
    Blogs.query.filter_by(slug=blog).delete()
    db.session.commit()
    flash('You deleted "%s". If you want to restore this blog, just type the name and all the posts reappear.' % blog)

def getPosts(blog):
    if Blogs.query.filter_by(slug=blog).all():
        blog_id = Blogs.query.filter_by(slug=blog).first()
        posts = BlogPosts.query.filter_by(blog=blog_id.id)
        return posts

def createaPost(form, blog):
    blog_id = Blogs.query.filter_by(slug=blog).first()
    newpost = BlogPosts(
    published=False,
    datePublished=form.date.data,
    title=form.title.data,
    slug=form.title.data.lower().replace(' ', '-'),
    description=form.description.data,
    image=form.image.data,
    author=form.author.data,
    category=form.category.data,
    blog=blog_id.id,
    )
    db.session.add(newpost)
    db.session.commit()
    flash('You created the post %s! This post is not yet published. Click the post to edit it\'s data and content.' % form.title.data)

def editaPost(form, blog, post):
    blog_id = Blogs.query.filter_by(slug=blog).first()
    _post = BlogPosts.query.filter_by(slug=post).first()
    _post.datePublished=form.date.data
    _post.title=form.title.data
    _post.description=form.description.data
    _post.image=form.image.data
    _post.author=form.author.data
    _post.category=form.category.data
    _post.blog=blog_id.id
    db.session.add(_post)
    db.session.commit()
    flash('Edited settings for %s' % form.title.data)

def deleteaPost(post):
    BlogPosts.query.filter_by(slug=post).delete()
    db.session.commit()
    flash('You deleted "%s".' % post)
