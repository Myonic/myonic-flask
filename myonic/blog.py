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
   
