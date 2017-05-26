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

class OAuth(OAuthConsumerMixin, db.Model):
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'))
    user        = db.relationship('Users')

class BlogPost(db.Model):
    __tablename__ = 'posts'
    id          = db.Column(db.Integer, primary_key = True)
    postDate    = db.Column(db.String)
    published   = db.Column(db.Boolean)
    content     = db.Column(db.String)
    publishedBy = db.Column(db.String)
    category    = db.Column(db.String)
    blog        = db.Column(db.Integer, db.ForeignKey('blogs.id'))
    isPage      = db.Column(db.Boolean)

class Blog(db.Model):
    __tablename__ = 'blogs'
    id          = db.Column(db.Integer, primary_key = True)
    name        = db.Column(db.String)
    posts       = db.relationship('BlogPost', backref='blogs', lazy='dynamic')
