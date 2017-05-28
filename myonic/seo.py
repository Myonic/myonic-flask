# SEO Content Generation System
from flask import jsonify
from myonic import app

def getSiteInfo():
    site_twitter = app.config.get('SITE_TWITTER')
    site_facebook = app.config.get('SITE_FACEBOOK')
    site_youtube = app.config.get('SITE_YOUTUBE')
    site_url = app.config.get('SITE_URL')
    site_name = app.config.get('SITE_NAME')
    return dict(site_twitter=site_twitter, site_facebook=site_facebook, site_youtube=site_youtube, site_url=site_url, site_name=site_name)
