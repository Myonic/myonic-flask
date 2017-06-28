# SEO Content Generation System
import json
from myonic import app
import datetime

@app.context_processor
def schemaProcessor():
    def getPostSchema(post):
        # TODO: Add Breadcrumbs and Navigation stuffs
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
                'name': post.users.first_name + ' ' + post.users.last_name,
                'image': post.users.picture,
                # 'url': post.author.url,
                # 'sameAs': post.url, # TODO: Figure out how to pass post URL
                'description': post.users.bio
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
        return json.dumps(schema, indent=4, sort_keys=True)

    def getHomeSchema():
        schema = {
            '@context': 'https://schema.org',
            '@type': 'Website',
            'publisher': {
                '@type': 'Organization',
                'name': app.config.get('SITE_NAME'),
                # 'logo': app.config.get('SITE_LOGO') #TODO: Site logo
            },
            'url': app.config.get('SITE_DOMAIN'),
            # 'image': #[SITE COVER IMAGE], #TODO: Site Cover Image
            'mainEntityOfPage': {
                '@type': 'WebPage',
                '@id': app.config.get('SITE_DOMAIN')
            },
            'description': app.config.get('SITE_DESCRIPTION')
        }
        return json.dumps(schema, indent=4, sort_keys=True)

    def getPageSchema(page):
        schema = {
            '@context': 'https://schema.org',
            '@type': 'Website',
            'publisher': {
                '@type': 'Organization',
                'name': app.config.get('SITE_NAME'),
                # 'logo': app.config.get('SITE_LOGO') #TODO: Site logo
            },
            'url': app.config.get('SITE_DOMAIN'),
            # 'image': #[SITE COVER IMAGE], #TODO: Site Cover Image
            'mainEntityOfPage': {
                '@type': 'WebPage',
                '@id': app.config.get('SITE_DOMAIN'),
                'name': page.title,
                'description': page.description #,
                # 'breadcrumb' : page.breadcrumb,
                # 'image' : page.image #TODO: Page Featured Image
            },
            'description': app.config.get('SITE_DESCRIPTION')
        }
        return json.dumps(schema, indent=4, sort_keys=True)

    return dict(getPageSchema=getPageSchema, getPostSchema=getPostSchema, getHomeSchema=getHomeSchema)

class articleSEO():
    def __init__(self, title, postDate, author, category, twitter_type, description=None, type='article', image=None, author_twitter=None):
        '''
        SEO GUIDELINES
            NOTE:
                Pass output to var SEO
                Ex: render_template('example.html.j2', SEO=SEOconfig())
            Required Fields:
                title : Text
                author : Text
                category : Text
                postDate : datetime > ISO 8601
                twitter_type : "summary" or "summary_large_image"
            Optional Fields:
                author_twitter : Text
                image : URL
        '''
        self.title=title
        self.description=description
        self.type=type
        self.image=image
        self.postDate=postDate
        self.author=author
        self.category=category
        self.author_twitter=author_twitter
        self.twitter_type=twitter_type
    # return dict(title=title, description=description, type=type, image=image, postDate=postDate, author=author, category=category, author_twitter=author_twitter, twitter_type=twitter_type)

class pageSEO():
    def __init__(self, title, description=None, type='website', image=None, twitter_type='summary'):
        '''
        SEO GUIDELINES
            NOTE:
                Pass output to var SEO
                Ex: render_template('example.html.j2', SEO=SEOconfig())
            Required Fields:
                title : Text
                twitter_type : "summary" or "summary_large_image"
            Optional Fields:
                description : Text
                image : URL
        '''
        self.title=title
        self.description=description
        self.type=type
        self.image=image
        self.twitter_type=twitter_type
    # return dict(title=title, description=description, type=type, image=image, twitter_type=twitter_type)
