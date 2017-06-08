from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, HiddenField
from wtforms.validators import DataRequired, URL, Email, ValidationError
from wtforms.ext.dateutil.fields import DateTimeField
from myonic.models import BlogPosts

def TitleCheck(form, field):
    if BlogPosts.query.filter_by(title=field.data.capitalize()).all():
        raise ValidationError('Post title already exists')

# Only load needed fields for articles and pages
class editPostForm(FlaskForm):
    published = BooleanField('Published?')
    title = StringField('Title', validators=[DataRequired(message='The post must have a title'), TitleCheck])
    description = StringField('Short Description')
    date = DateTimeField('Date Published (UTC)')
    image = StringField('Image', validators=[URL(message='Image must be from a URL')])
    author = StringField('Author Email', validators=[Email(message="Author must be an email")])
    category = StringField('Category')
    blog = HiddenField() # Name of blog
    isPage = BooleanField('Set as Page') # Check this as true on page creation template
    pageRoute = StringField('Page Path')
