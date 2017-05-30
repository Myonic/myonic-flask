# SEO Content Generation System
import json
from myonic import app
import datetime

def getSiteInfo():
    site_twitter = app.config.get('SITE_TWITTER')
    site_facebook = app.config.get('SITE_FACEBOOK')
    site_youtube = app.config.get('SITE_YOUTUBE')
    site_url = app.config.get('SITE_DOMAIN')
    site_name = app.config.get('SITE_NAME')
    return dict(site_twitter=site_twitter, site_facebook=site_facebook, site_youtube=site_youtube, site_url=site_url, site_name=site_name)

def getPostSchema(post):
    schema = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'publisher': {
            '@type': 'Organization',
            'name': app.config.get('SITE_NAME') #,
            # 'logo': app.config.get('SITE_LOGO')
        },
        'author': {
            '@type': 'Person',
            'name': post.author.first_name + ' ' + post.author.last_name,
            'image': post.author.picture,
            # 'url': post.author.url,
            # 'sameAs': post.url, # TODO: Figure out how to pass post URL
            'description': post.author.bio
        },
        'headline': post.title,
        # 'url': post.url, # TODO: Figure out how to pass post URL
        'datePublished': post.datePublished.isoformat(),
        # 'dateModified': metaData.dateModified.isoformat(),
        'image': post.image,
        # 'keywords': post.tags,
        'description': post.description,
        'mainEntityOfPage': {
            '@type': 'WebPage',
            '@id': app.config.get('SITE_DOMAIN')
        }
    }
    return json.dumps(schema, indent=4)

def getHomeSchema():
        schema = {
            '@context': 'https://schema.org',
            '@type': 'Website',
            'publisher': {
                '@type': 'Organization',
                'name': app.config.get('SITE_NAME'),
                # 'logo': app.config.get('SITE_LOGO')
            },
            'url': app.config.get('SITE_DOMAIN'),
            # 'image': #[SITE COVER IMAGE],
            'mainEntityOfPage': {
                '@type': 'WebPage',
                '@id': app.config.get('SITE_DOMAIN')
            },
            'description': app.config.get('SITE_DESCRIPTION')
        }
