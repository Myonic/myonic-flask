from myonic import app
import os

SECRET_KEY = 'secret'
SQLALCHEMY_DATABASE_URI = 'sqlite:///myonic.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER      = 'static/images/'
THUMBS_FOLDER      = 'static/thumbs/'
ALLOWED_EXTENSIONS =  set(['png','jpg','jpeg','gif', 'css'])
#TODO: Set this to use os.eviron maybe?
if app.debug:
    GOOGLE_CLIENT_ID = '829851563990-35t7op4btrdhrj9duameklqjjo2i8t0o.apps.googleusercontent.com' # Will work on localhost:5000 or 127.0.0.1:5000
    GOOGLE_SECRET = '1u1ZRyhuAOaMerY_wSYpl6mh' # Will work on localhost:5000 or 127.0.0.1:5000
else:
    GOOGLE_CLIENT_ID = '829851563990-cd6u0qhfil77ltb1vfhc3ps1r38jm74h.apps.googleusercontent.com' # WILL ONLY WORK IN PRODUCTION (MYONIC.TECH DOMAIN)
    GOOGLE_SECRET = 'ZFDP87r80-vVIerbGjyGUS0a' # WILL ONLY WORK IN PRODUCTION (MYONIC.TECH DOMAIN)
