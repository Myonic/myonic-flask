from flask import  Flask, abort, flash, redirect, render_template, request, url_for, request, Response
from myonic import app
from myonic.models import *

def getblogs():
    blogs = Blogs.query.all()
    return blogs
def newblog(name):
    newblog = Blogs(name = name)
    db.session.add(newblog)
    db.session.commit()
