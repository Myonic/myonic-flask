from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, HiddenField
from wtforms.validators import DataRequired, URL, Email, ValidationError, Regexp
from wtforms.ext.dateutil.fields import DateField
from myonic.models import Pages, Posts

# TODO: Add length validators to prevent database errors

def createPagePathCheck(form, field):
    if Pages.query.filter_by(path=field.data).all() or field.data == '/':
        raise ValidationError('Page path already exists')
    if field.data.startswith('/admin'):
        raise ValidationError('Page cannot be in a /admin path')


# Only load needed fields for articles and pages
class createPageForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message='The page must have a title')])
    path = StringField('Path', validators=[DataRequired(message='The page must have a path'), createPagePathCheck, Regexp('^/([a-z\/]+)', message='The path is not valid. It must start with a "/" and only have lower case letters.')])
    description = StringField('Short Description')

def editPagePathCheck(form, field):
    if Pages.query.filter_by(id=int(form.id.data)).first().id != int(form.id.data) and (Pages.query.filter_by(path=field.data).first() != None or field.data == '/'):
        raise ValidationError('Page path already exists')
    if field.data.startswith('/admin'):
        raise ValidationError('Page cannot be in a /admin path')


# Only load needed fields for articles and pages
class editPageForm(FlaskForm):
    published = BooleanField('Published?')
    # title = StringField('Title', validators=[DataRequired(message='The page must have a title')])
    path = StringField('Path', validators=[DataRequired(message='The page must have a path'), editPagePathCheck, Regexp('^/([a-z\/]+)', message='The path is not valid. It must start with a "/" and only have lower case letters.')])
    description = StringField('Summery')
    id = HiddenField()

def postTitleCheck(form, field):
    if Posts.query.filter_by(title=field.data).all():
        raise ValidationError('There is already a post with that title')

class createPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message='The post must have a title'), postTitleCheck])
    date = DateField('Date')
    description = StringField('Short Description')
    category = SelectField('Category', coerce=int) # TODO: Validate this field
    tags = StringField('Tags')

class editPostForm(FlaskForm):
    published = BooleanField('Published?')
    date = DateField('Date')
    description = StringField('Short Description')
    category = SelectField('Category', coerce=int) # TODO: Validate this field
    tags = StringField('Tags')
    author = SelectField('Author', coerce=int) # TODO: Validate this field

class createCategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message='Please provide a name for the category')])

# class userDataForm(FlaskForm):
#     twitter = StringField('Twitter Account')
#     bio = StringField('Short Bio')
