from flask import  Flask, abort, flash, redirect, render_template, request, url_for, request, Response
from myonic import app
from myonic.models import *

def getBlogs():
    blogs = Blogs.query.all()
    return blogs

def newBlog(name):
    if not Blogs.query.filter_by(name=name.capitalize()).all():
        newblog = Blogs(name = name.capitalize())
        db.session.add(newblog)
        db.session.commit()
        flash('You created the blog %s!' % name.capitalize)
    else:
        flash('A blog with that name already exsists')

def deleteBlog(blog):
    Blogs.query.filter_by(name=blog).delete()
    db.session.commit()
    flash('You deleted "%s". If you want to restore this blog, just type the name and all the posts reappear.' % blog)

def getPosts(blog):
    if Blogs.query.filter_by(name=blog).all():
        blog_id = Blogs.query.filter_by(name=blog).first()
        posts = BlogPosts.query.filter_by(blog=blog_id.id)
        return posts

def createPost(form, blog):
    blog_id = Blogs.query.filter_by(name=blog).first()
    newpost = BlogPosts(
    published=False,
    datePublished=form.date.data,
    title=form.title.data.capitalize(),
    description=form.description.data,
    image=form.image.data,
    author=form.author.data,
    category=form.category.data,
    blog=blog_id.id,
    )
    db.session.add(newpost)
    db.session.commit()
    flash('You created the post %s! This post is not yet published. Click the post to edit it\'s data and content.' % form.title.data.capitalize())

def editPost(form):
    post = BlogPosts.query.filter_by(form.title.data)
    post.datePublished=form.date.data
    post.title=form.title.data.capitalize()
    post.description=form.description.data
    post.image=form.image.data
    post.author=form.author.data
    post.category=form.category.data
    post.blog=blog_id.id
    db.session.commit()
    flash('Edited settings for %s' % form.title.data.capitalize())

def deletePost(post):
    BlogPosts.query.filter_by(title=post).delete()
    db.session.commit()
    flash('You deleted "%s".' % post)

    
