from datetime import datetime
import sys, os, random, string, imp
from flask import Flask, abort, flash, redirect, render_template, request, url_for, request, Response
from sqlalchemy.orm.exc import NoResultFound
from functools import wraps
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from migrate.versioning import api
from .models import *

#TODO: Database Migrations
#TODO: File logs of errors and user activity

app = Flask(__name__)

app.config.from_pyfile('configs.py')

login_manager = LoginManager()
login_manager.login_view = 'google.login'

from configs import *
from util import *

# --- User Auth and Session System ---

# Google API
# NOTE:
blueprint = make_google_blueprint(
    client_id=app.config.get('GOOGLE_CLIENT_ID'),
    client_secret=app.config.get('GOOGLE_SECRET'),
    scope=["profile", "email"]
)
app.register_blueprint(blueprint, url_prefix="/login")

blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@oauth_authorized.connect_via(blueprint)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with {name}".format(name=blueprint.name))
        return
    resp = blueprint.session.get("/oauth2/v2/userinfo")
    if resp.ok:
        try:
            if resp.json()["hd"] == "myonic.tech":
                print resp.json()
                email = resp.json()["email"]
                first_name = resp.json()["given_name"]
                last_name = resp.json()["family_name"]
                picture = resp.json()["picture"]
                query = Users.query.filter_by(email=email)
                try:
                    user = query.one()
                except NoResultFound:
                    user = Users(email=email, first_name=first_name, last_name=last_name, picture=picture)
                    db.session.add(user)
                    db.session.commit()
                login_user(user)
                flash("Successfully signed in with Google")
            else:
                flash("Please login with a myonic.tech Google Account")
        except KeyError:
            flash("Please login with a myonic.tech Google Account")
    else:
        msg = "Failed to fetch user info from {name}".format(name=blueprint.name)
        flash(msg, category="error")

@oauth_error.connect_via(blueprint)
def google_error(blueprint, error, error_description=None, error_uri=None):
    msg = (
        "OAuth error from {name}! "
        "error={error} description={description} uri={uri}"
    ).format(
        name=blueprint.name,
        error=error,
        description=error_description,
        uri=error_uri,
    )
    flash(msg, category="error")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("index"))

@app.route("/login")
def index():
    return render_template('login.html')

# --- Datebase Management ---

SQLALCHEMY_DATABASE_URI = app.config.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_MIGRATE_REPO = app.config.get('SQLALCHEMY_MIGRATE_REPO')

@app.cli.command()
def initdb():
    if not os.path.exists(SQLALCHEMY_DATABASE_URI):
        db.create_all()
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
    print("Database created")

@app.cli.command()
def downgradedb():
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print('Current database version: ' + str(v))

@app.cli.command()
def migratedb():
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v + 1))
    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    exec (old_model, tmp_module.__dict__)
    script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
    open(migration, "wt").write(script)
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print('New migration saved as ' + migration)
    print('Current database version: ' + str(v))

@app.cli.command()
def upgradedb():
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print('Current database version: ' + str(v))

db.init_app(app)
login_manager.init_app(app)
