from app import db

class Users(db.Model):
    __tablename__ = 'users'
    id        = db.Column(db.Integer, primary_key = True)
    username   = db.Column(db.String)
    email     = db.Column(db.String)
    pw_hash   = db.Column(db.String)

class BlogPost(db.Model):
    __tablename__ = 'post'
    id        = db.Column(db.Integer, primary_key = True)
    postDate = db.Column(db.String) 
    published = db.Column(db.Boolean)
    content   = db.Column(db.String)
    publishedBy = db.Column(db.String)
    category    = db.Column(db.String)
    blog        = db.Column(db.Integer, db.ForeignKey('blog.id'))
    isPage      = db.Column(db.Boolean)
    
class Blog(db.Model):
    __tablename__ = 'blog'
    id        = db.Column(db.Integer, primary_key = True)
    name      = db.Column(db.String)
    posts     = db.relationship('BlogPost', backref='blog', lazy='dynamic')
    
