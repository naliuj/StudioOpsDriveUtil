from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class RenameForm(FlaskForm):
    id = StringField('ID')
    folder = StringField('Folder')
    newName = StringField('New Name')
    submit = SubmitField('Submit')
