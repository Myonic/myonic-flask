from app import db

class Users(db.Model):
    __tablename__ = 'users'
    id        = db.Column(db.Integer, primary_key = True)
    username   = db.Column(db.String)
    pw_hash   = db.Column(db.String)


