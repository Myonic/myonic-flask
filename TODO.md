## [TODO](https://docs.google.com/a/myonictechnologies.com/document/d/1GB5TynLs-_GnDuHKx0f23URxWyeD57Hy477ZhmzysFE/edit?usp=sharing)
* Figure out how to edit posts in client timezone instead of UTC
  * Use [moment.js](https://momentjs.com/) to modify timezones in BOTH the editor and on the post. Otherwise dates may be off in the published post.
* [Sitemap Generation](https://pythonprogramming.net/flask-seo-tutorial/)
* [Dynamic WTF-forms](https://stackoverflow.com/questions/22203159/generate-a-dynamic-form-using-flask-wtf-and-sqlalchemy)
* Admin Panel
  * [Access Management](http://pythonhosted.org/Flask-Principal/)
  * Add GUI (display profile pic)
  * User type (admin, superadmin)
* Navigation System
* Newsletter System
* Page System
* Blog System
  * Change delete button on blog to unpublish (and add published state to blog model). Fully deleting a blog will only be avalible to high level users.
  * Change delete button on post to unpublish and allow deleting post after unpublish.
  * Peer review system where post/page cannot be published without review
* Templates
  * Base Layout (layout.html)
  * Homepage Layout
* Change Favicon
* Change site config (in config.py) through admin panel
* [Generate sitemap.xml](http://flask.pocoo.org/snippets/108/)
* [Generate RSS feed for each blog](http://flask.pocoo.org/snippets/10/)
* Social buttons
* Automate `sqlalchemy_utils` db fix with `setup.py`
  * Automate init database with `setup.py`
