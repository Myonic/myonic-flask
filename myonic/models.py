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
    posts       = db.relationship('Posts', backref='users', lazy='dynamic') # TODO: update backref name

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
    navitems    = db.relationship('Navbar', backref='pageitem', lazy='dynamic')

class Posts(db.Model):
    __tablename__ = 'posts'
    id          = db.Column(db.Integer, primary_key = True)
    datePublished = db.Column(db.Date)  # Date of publication Uses DateTime object to allow conversion to different formats (do not include in pages)
    published   = db.Column(db.Boolean)     # Published state
    title       = db.Column(db.String(256))
    slug        = db.Column(db.String(256), unique=True)
    content     = db.Column(db.String)
    description = db.Column(db.String(256)) # Short description of page or article
    image       = db.Column(db.String(256)) # Featured image on the post
    author      = db.Column(db.String, db.ForeignKey('users.email'))  # Author (do not include in pages)
    category    = db.Column(db.Integer, db.ForeignKey('categories.id'))  # Category of post (do not include in pages)
    tags        = db.Column(db.PickleType)

class Categories(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    name        = db.Column(db.String(256), unique = True)
    posts       = db.relationship('Posts', backref='categories', lazy='dynamic') # TODO: update backref name

class Navbar(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    index       = db.Column(db.Integer)
    label       = db.Column(db.String)
    type        = db.Column(db.String) # "url" or "page" (TODO: or "dropdown" or "seperator" or "label" when dropdown support is added)
    url         = db.Column(db.String)
    page        = db.Column(db.Integer, db.ForeignKey('pages.id'))

class Site(db.Model):
    __tablename__ = 'site'
    id          = db.Column(db.Integer, primary_key = True)
    setting        = db.Column(db.String(256))
    data           = db.Column(db.String(256))
