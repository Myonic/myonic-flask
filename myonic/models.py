from flask_login import UserMixin, current_user
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin, SQLAlchemyBackend
from flask_sqlalchemy import SQLAlchemy
from myonic import app
from flask_migrate import Migrate

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id          = db.Column(db.Integer, primary_key = True)
    first_name  = db.Column(db.String(256))
    last_name   = db.Column(db.String(256))
    picture     = db.Column(db.String(256)) # Stored as URL from Google
    email       = db.Column(db.String(256), unique = True)
    twitter     = db.Column(db.String(256)) # User Twitter account (EX: @myonic)
    bio         = db.Column(db.String)
    posts       = db.relationship('BlogPost', backref='users', lazy='dynamic')

class OAuth(OAuthConsumerMixin, db.Model):
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'))
    user        = db.relationship('Users')

class BlogPost(db.Model):
    __tablename__ = 'posts'
    id          = db.Column(db.Integer, primary_key = True)
    datePublished = db.Column(db.DateTime(timezone = True))  # Date of publication Uses DateTime object to allow conversion to different formats (do not include in pages)
    published   = db.Column(db.Boolean)     # Published state
    title       = db.Column(db.String(256))
    content     = db.Column(db.String)      # Content limited to 4096
    description = db.Column(db.String(256)) # Short description of page or article
    image       = db.Column(db.String(256)) # Featured image on the post
    author      = db.Column(db.String(256), db.ForeignKey('users.id'))  # Author (do not include in pages)
    category    = db.Column(db.String(32))  # Category of post (do not include in pages)
    blog        = db.Column(db.Integer, db.ForeignKey('blogs.id')) # Blog relationship (do not include in pages)
    isPage      = db.Column(db.Boolean)     # Determines if post is treated as page on site
    pageRoute   = db.Column(db.String(256)) # Appended to default route (pages only)

class Blog(db.Model):
    __tablename__ = 'blogs'
    id          = db.Column(db.Integer, primary_key = True)
    name        = db.Column(db.String(32))  # Name of blog
    posts       = db.relationship('BlogPost', backref='blogs', lazy='dynamic')
