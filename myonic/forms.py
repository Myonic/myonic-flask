from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, HiddenField
from wtforms.validators import DataRequired, URL, Email, ValidationError, Regexp
from wtforms.ext.dateutil.fields import DateTimeField
from myonic.models import Pages

def CreatePathCheck(form, field):
    if Pages.query.filter_by(path=field.data).all() or field.data == '/':
        raise ValidationError('Page path already exists')
    if field.data.startswith('/admin'):
        raise ValidationError('Page cannot be in a /admin path')


# Only load needed fields for articles and pages
class createPageForm(FlaskForm):
    published = BooleanField('Published?')
    title = StringField('Title', validators=[DataRequired(message='The page must have a title')])
    path = StringField('Path', validators=[DataRequired(message='The page must have a path'), CreatePathCheck, Regexp('^/([a-z\/]+)', message='The path is not valid. It must start with a "/" and only have lower case letters.')])
    description = StringField('Short Description')
    id = HiddenField()

def EditPathCheck(form, field):
    if Pages.query.filter_by(id=int(form.id.data)).first().id != int(form.id.data) and (Pages.query.filter_by(path=field.data).first() != None or field.data == '/'):
        raise ValidationError('Page path already exists')
    if field.data.startswith('/admin'):
        raise ValidationError('Page cannot be in a /admin path')


# Only load needed fields for articles and pages
class editPageForm(FlaskForm):
    published = BooleanField('Published?')
    # title = StringField('Title', validators=[DataRequired(message='The page must have a title')])
    path = StringField('Path', validators=[DataRequired(message='The page must have a path'), EditPathCheck, Regexp('^/([a-z\/]+)', message='The path is not valid. It must start with a "/" and only have lower case letters.')])
    description = StringField('Summery')
    id = HiddenField()
