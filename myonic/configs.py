from myonic import app
import os
from datetime import timedelta

SQLALCHEMY_DATABASE_URI = 'sqlite:///database/myonic.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER      = 'static/uploads/'
ALLOWED_EXTENSIONS =  set(['png','jpg','jpeg','gif'])
REMEMBER_COOKIE_DURATION = timedelta(days=1)
REMEMBER_COOKIE_DOMAIN = '.127.0.0.1'
# TODO: Eventually set secret/client_id to use Enviroment Variables
if app.debug:
    SECRET_KEY = 'secret'
    SERVER_NAME = 'localhost:5000'
    GOOGLE_CLIENT_ID = '829851563990-35t7op4btrdhrj9duameklqjjo2i8t0o.apps.googleusercontent.com' # Add a key that will work on localhost:5000 or 127.0.0.1:5000
    GOOGLE_SECRET = '1u1ZRyhuAOaMerY_wSYpl6mh' # Add a key that will on localhost:5000 or 127.0.0.1:5000
else:
    SECRET_KEY = os.urandom(24).encode('hex')
    GOOGLE_CLIENT_ID = '829851563990-cd6u0qhfil77ltb1vfhc3ps1r38jm74h.apps.googleusercontent.com' # Add a key that will only work on your production domain (ex: example.com or subdomain.example.com)
    GOOGLE_SECRET = 'ZFDP87r80-vVIerbGjyGUS0a' # Add a key that will only work on your production domain (ex: example.com or subdomain.example.com)

# --- Site Config ---
# TODO: Set this to be updatable from within the admin panel
# NOTE: When updated from the admin panel, this data is injected into the config. Data is injected into the config on app start as well.
SITE_NAME = 'Myonic Technologies'

# Social Accounts
SITE_TWITTER = '@myonic' #Ex: @twitter
SITE_FACEBOOK = ''
SITE_YOUTUBE = ''

# Contact
SITE_EMAIL = 'contact@myonic.tech'
SITE_PHONE = ''

# Info
SITE_OWNER = 'Myonic Technologies Inc.' # Publisher Name
SITE_DOMAIN = 'http://myonic.tech/' # Ex: http://example.com/
SITE_DESCRIPTION = "We've designed a wearable device that allows paralyzed users to regain control of their muscles."
