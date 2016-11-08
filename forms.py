from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class EntryForm(FlaskForm):
    title = StringField('title', )
    slug
    content
    published
    timestamp
