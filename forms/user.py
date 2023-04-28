from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, PasswordField, StringField, SubmitField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = StringField('Login / email', validators={DataRequired()})
    password = PasswordField('Password', validators={DataRequired()})
    password_again = PasswordField('Repeat password', validators={DataRequired()})
    surname = StringField('Surname', validators={DataRequired()})
    name = StringField('Name', validators={DataRequired()})
    age = IntegerField('Age', validators={DataRequired()})
    position = StringField('Position', validators={DataRequired()})
    speciality = StringField('Speciality', validators={DataRequired()})
    address = StringField('Address', validators={DataRequired()})
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')
