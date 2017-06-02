from flask import  Flask, abort, flash, redirect, render_template, request, url_for, request, Response
from myonic import app
from myonic.models import *

def getBlogs():
    blogs = Blogs.query.all()
    return blogs

def newBlog(name):
    if not db.session.query(Blogs).filter_by(name=name).all():
        newblog = Blogs(name = name)
        db.session.add(newblog)
        db.session.commit()
    else:
        pass

def deleteBlog(blog):
    db.session.query(Blogs).filter_by(name=blog).delete()
    db.session.commit()

def getPosts(blog):
    blog_id = Blogs.query.filter_by(name=blog).first()
    posts = BlogPosts.query.filter_by(blog=blog_id.id)
    return posts

def createPost(form, blog):
    blog_id = Blogs.query.filter_by(name=blog).first()
    newpost = BlogPosts(
    datePublished=form.date.data,
    title=form.title.data,
    description=form.description.data,
    image=form.image.data,
    author=form.author.data,
    category=form.category.data,
    blog=blog_id.id,
    )
    db.session.add(newpost)
    db.session.commit()
