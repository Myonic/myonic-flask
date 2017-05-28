from flask_login import UserMixin, current_user
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin, SQLAlchemyBackend
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id          = db.Column(db.Integer, primary_key = True)
    first_name  = db.Column(db.String(256))
    last_name   = db.Column(db.String(256))
    picture     = db.Column(db.String(256)) # Stored as URL from Google
    email       = db.Column(db.String(256), unique = True)
    twitter     = db.Column(db.String(256)) # User Twitter account (EX: @myonic)

class OAuth(OAuthConsumerMixin, db.Model):
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'))
    user        = db.relationship('Users')

class BlogPost(db.Model):
    __tablename__ = 'posts'
    id          = db.Column(db.Integer, primary_key = True)
    postDate    = db.Column(db.String(32))  # Date of publication (do not include in pages)
    published   = db.Column(db.Boolean)     # Published state
    title       = db.Column(db.String(256))
    content     = db.Column(db.String(4096))# Content limited to 4096
    description = db.Column(db.String(256)) # Short description of page or article
    images      = db.Column(db.String(256)) # Featured image on the post
    publishedBy = db.Column(db.String(32))  # Author (do not include in pages)
    category    = db.Column(db.String(32))  # Category of post (do not include in pages)
    blog        = db.Column(db.Integer, db.ForeignKey('blogs.id')) # Blog relationship (do not include in pages)
    isPage      = db.Column(db.Boolean)     # Determines if post is treated as page on site
    pageRoute   = db.Column(db.String(256)) # Appended to default route (pages only)

class Blog(db.Model):
    __tablename__ = 'blogs'
    id          = db.Column(db.Integer, primary_key = True)
    name        = db.Column(db.String(32))  # Name of blog
    posts       = db.relationship('BlogPost', backref='blogs', lazy='dynamic')
