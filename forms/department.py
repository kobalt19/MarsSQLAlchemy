from flask_wtf import FlaskForm
from wtforms import EmailField, SelectField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import DataRequired


class AddDepForm(FlaskForm):
    title = StringField('Title', validators={DataRequired()})
    chief = SelectField('Chief', validate_choice=False)
    members = SelectMultipleField('Members', validate_choice=False)
    email = EmailField('Email', validators={DataRequired()})
    submit = SubmitField('Submit')
