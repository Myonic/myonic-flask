from flask import Flask, abort, flash, redirect, render_template, request, url_for, request, Response
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from sqlalchemy.orm.exc import NoResultFound
from myonic import app, login_manager
from models import *

# --- User Auth and Session System ---

# Google API
# NOTE:
blueprint = make_google_blueprint(
    client_id=app.config.get('GOOGLE_CLIENT_ID'),
    client_secret=app.config.get('GOOGLE_SECRET'),
    scope=['profile', 'email']
)
app.register_blueprint(blueprint, url_prefix='/login')

blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@oauth_authorized.connect_via(blueprint)
def google_logged_in(blueprint, token):
    if not token:
        flash('Failed to log in with {name}'.format(name=blueprint.name))
        return
    resp = blueprint.session.get('/oauth2/v2/userinfo')
    if resp.ok:
        try:
            if resp.json()['hd'] == 'myonic.tech':
                email = resp.json()['email']
                first_name = resp.json()['given_name']
                last_name = resp.json()['family_name']
                picture = resp.json()['picture']
                query = Users.query.filter_by(email=email)
                try:
                    user = query.one()
                except NoResultFound:
                    user = Users(email=email, first_name=first_name, last_name=last_name, picture=picture)
                    db.session.add(user)
                    db.session.commit()
                login_user(user)
                flash('Successfully signed in with Google')
            else:
                flash('Please login with a myonic.tech Google Account')
        except KeyError:
            flash('Please login with a myonic.tech Google Account')
    else:
        msg = 'Failed to fetch user info from {name}'.format(name=blueprint.name)
        flash(msg, category='error')

@oauth_error.connect_via(blueprint)
def google_error(blueprint, error, error_description=None, error_uri=None):
    msg = (
        'OAuth error from {name}! '
        'error={error} description={description} uri={uri}'
    ).format(
        name=blueprint.name,
        error=error,
        description=error_description,
        uri=error_uri,
    )
    flash(msg, category='error')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out')
    return redirect(url_for('index'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/')
def index():
    return redirect(url_for('login'))
