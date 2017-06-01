# Myonic CMS
A rewrite of the Myonic website in Python/Flask.

## Setup
1. Create a virtualenv
  1. Run `virtualenv [ENV]`
  2. Activate with `source bin/activate` to work within the environment (to deactivate just type `deactivate`)
2. Run `python setup.py install`
3. Run `export FLASK_APP=[PATH TO __init__.py]`
4. *(Optional)* If you are running in a development environment, run `export FLASK_DEBUG=true` but **DO NOT USE IN PRODUCTION**
  * For login to work on `localhost` run `export OAUTHLIB_INSECURE_TRANSPORT=1` and `export OAUTHLIB_RELAX_TOKEN_SCOPE=1`
5. Run `flask db migrate` then `flask db upgrade` to create the database
7. To run the app type `flask run`

*On local development environments, you must set `export OAUTHLIB_INSECURE_TRANSPORT=1` and `export OAUTHLIB_RELAX_TOKEN_SCOPE=1` in order for the Google auth to function properly but* ***DO NOT DO USE IN PRODUCTION***

## Other Stuff
* Run Flask in shell mode: `flask shell`
* Database
  * Migrate database: `flask db migrate`
  * Upgrade database: `flask db upgrade`
  * More database tools: `flask db --help`
