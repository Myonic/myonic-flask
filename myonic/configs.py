from myonic import app
import os

# TODO: Make secret key auto generate!!!
SECRET_KEY = os.environ['SECRET_KEY']
SQLALCHEMY_DATABASE_URI = 'sqlite:///database/myonic.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER      = 'static/uploads/'
ALLOWED_EXTENSIONS =  set(['png','jpg','jpeg','gif', 'css'])
# TODO: Eventually set secret/client_id to use Enviroment Variables
if app.debug:
    GOOGLE_CLIENT_ID = '829851563990-35t7op4btrdhrj9duameklqjjo2i8t0o.apps.googleusercontent.com' # Will work on localhost:5000 or 127.0.0.1:5000
    GOOGLE_SECRET = '1u1ZRyhuAOaMerY_wSYpl6mh' # Will work on localhost:5000 or 127.0.0.1:5000
else:
    GOOGLE_CLIENT_ID = '829851563990-cd6u0qhfil77ltb1vfhc3ps1r38jm74h.apps.googleusercontent.com' # WILL ONLY WORK IN PRODUCTION (MYONIC.TECH DOMAIN)
    GOOGLE_SECRET = 'ZFDP87r80-vVIerbGjyGUS0a' # WILL ONLY WORK IN PRODUCTION (MYONIC.TECH DOMAIN)

# --- Site Config ---
# TODO: Set this to be updatable from within the admin panel
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
