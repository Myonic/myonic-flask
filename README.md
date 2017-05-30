# Myonic CMS
A rewrite of the Myonic website in Python/Flask.

## Setup
1. Create a virtualenv
  1. Run `virtualenv [ENV]`
  2. Activate with `source bin/activate` to work within the environment (to deactivate just type `deactivate`)
2. Run `python setup.py install`
3. Run `export FLASK_APP=[PATH TO __init__.py]`
4. *(Optional)* If you are running in a development environment, run `export FLASK_DEBUG=true` but **DO NOT USE IN PRODUCTION**
6. Create the database with `flask db init` *(Make sure you are in the app (myonic) directory)*
  1. Navigate to newly created `myonic/migrations` directory and edit `script.py.mako`
  2. Append `import sqlalchemy_utils` to the import list so you have:
  ```python
  from alembic import op
  import sqlalchemy as sa
  import sqlalchemy_utils
  ```
  3. Run `flask db upgrade`
7. To run the app type `flask run`

*On local development environments, you must set `export OAUTHLIB_INSECURE_TRANSPORT=1` and `export OAUTHLIB_RELAX_TOKEN_SCOPE=1` in order for the Google auth to function properly but* ***DO NOT DO USE IN PRODUCTION***

## Other Stuff
* Run Flask in shell mode: `flask shell`
* Database
  * Create database: `flask db init`
  * Migrate database: `flask db migrate`
  * Upgrade database: `flask db upgrade`
  * More database tools: `flask db --help`

## [TODO](https://docs.google.com/a/myonictechnologies.com/document/d/1GB5TynLs-_GnDuHKx0f23URxWyeD57Hy477ZhmzysFE/edit?usp=sharing)
* Check SEO is up to standards with Ghost SEO
  * [Sitemap Generation](https://pythonprogramming.net/flask-seo-tutorial/)
  * HTML Meta Tag Generation
* [Dynamic WTF-forms](https://stackoverflow.com/questions/22203159/generate-a-dynamic-form-using-flask-wtf-and-sqlalchemy)
* Admin Panel
  * [Access Management](http://pythonhosted.org/Flask-Principal/)
* Blog System
* Navigation System
* Newsletter System
* Page System
* Templates
  * Base Layout (layout.html)
  * Homepage Layout
* Favicon
* [Generate sitemap.xml](http://flask.pocoo.org/snippets/108/)
* [Generate RSS feed for each blog](http://flask.pocoo.org/snippets/10/)
* Social buttons
