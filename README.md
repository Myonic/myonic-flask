# Myonic CMS
A rewrite of the Myonic website in Python/Flask.

## Setup
1. Create a virtualenv
  1. Run `virtualenv [ENV]`
  2. Activate with `source bin/activate` to work within the environment (to deactivate just type `deactivate`)
2. Run `python setup.py install`
3. Run `export FLASK_APP=[PATH TO __init__.py]`
4. *(Optional)* If you are running in a development environment, run `export FLASK_DEBUG=true` **DO NOT USE IN PRODUCTION**
6. Create the database with `flask initdb`
7. To run the app type `flask run`

## Other Stuff
* Run Flask in shell mode: `flask shell`
* Database
  * Create database: `flask initdb`
  * Migrate database: `flask migratedb`
  * Upgrade database: `flask upgradedb`
  * Downgrade database: `flask downgradedb`
