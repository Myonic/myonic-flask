from flask_login import UserMixin, current_user
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin, SQLAlchemyBackend
from flask_sqlalchemy import SQLAlchemy
from myonic import app
from flask_migrate import Migrate

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: Eventaully switch to RethinkDB when more then just admins are using the system

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id          = db.Column(db.Integer, primary_key = True)
    first_name  = db.Column(db.String(256))
    last_name   = db.Column(db.String(256))
    picture     = db.Column(db.String(256)) # Stored as URL from Google
    email       = db.Column(db.String(256), unique = True)
    twitter     = db.Column(db.String(256)) # User Twitter account (EX: @myonic)
    bio         = db.Column(db.String)
    # timezone    = db.Column(db.String)
    posts       = db.relationship('Posts', backref='users', lazy='dynamic')

class OAuth(OAuthConsumerMixin, db.Model):
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'))
    user        = db.relationship('Users')

class Pages(db.Model):
    __tablename__ = 'pages'
    id          = db.Column(db.Integer, primary_key = True)
    published   = db.Column(db.Boolean)     # Published state
    title       = db.Column(db.String(256))
    content     = db.Column(db.String)
    description = db.Column(db.String(256)) # Short description of page or article
    image       = db.Column(db.String(256)) # Featured image on the post
    path        = db.Column(db.String(256), unique = True)

class Posts(db.Model):
    __tablename__ = 'posts'
    id          = db.Column(db.Integer, primary_key = True)
    datePublished = db.Column(db.Date)  # Date of publication Uses DateTime object to allow conversion to different formats (do not include in pages)
    published   = db.Column(db.Boolean)     # Published state
    title       = db.Column(db.String(256), unique=True)
    content     = db.Column(db.String)
    description = db.Column(db.String(256)) # Short description of page or article
    image       = db.Column(db.String(256)) # Featured image on the post
    author      = db.Column(db.Integer, db.ForeignKey('users.id'))  # Author (do not include in pages)
    category    = db.Column(db.Integer, db.ForeignKey('categories.id'))  # Category of post (do not include in pages)
    tags        = db.Column(db.PickleType)

class Categories(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    name        = db.Column(db.String(256), unique = True)
    posts       = db.relationship('Posts', backref='categories', lazy='dynamic')

class Site(db.Model):
    __tablename__ = 'site'
    id          = db.Column(db.Integer, primary_key = True)
    name        = db.Column(db.String(256))
    short_name  = db.Column(db.String(256))
    twitter     = db.Column(db.String(256))
    facebook    = db.Column(db.String(256))
    email       = db.Column(db.String(256))
    phone       = db.Column(db.String(256))
    owner       = db.Column(db.String(256))
    domain      = db.Column(db.String(256))
    description = db.Column(db.String(512))
    google_client_debug = db.Column(db.String(512))
    google_secret_debug = db.Column(db.String(512))
    google_client = db.Column(db.String(512))
    google_secret = db.Column(db.String(512))

# class Blogs(db.Model):
#     __tablename__ = 'blogs'
#     id          = db.Column(db.Integer, primary_key = True)
#     name        = db.Column(db.String(32), unique = True)  # Name of blog
#     slug        = db.Column(db.String(32), unique = True)
#     posts       = db.relationship('BlogPosts', backref='blogs', lazy='dynamic')
