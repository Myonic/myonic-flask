from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, BooleanField, SelectField, HiddenField
from wtforms.validators import DataRequired, URL, Email

# Only load needed fields for articles and pages
class editPost(FlaskForm):
    published = BooleanField('Published?')
    title = StringField('Title', validators=[DataRequired(message='The post must have a title')])
    description = StringField('Short Description')
    date = DateTimeField('Date Published')
    image = StringField('Image', validators=[URL(message='Image must be from a URL')])
    author = StringField('Author Email', validators=[Email(message="Author must be an email")])
    category = StringField('Category')
    blog = HiddenField() # Name of blog
    isPage = BooleanField('Set as Page') # Check this as true on page creation template
    pageRoute = StringField('Page Path')
