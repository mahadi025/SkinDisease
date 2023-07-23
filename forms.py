from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import InputRequired
from wtforms import StringField, PasswordField




class UserRegistrationLoginForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    password1 = PasswordField('Password1', validators=[InputRequired()])
    password2 = PasswordField('Password2', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])



class UserLoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])


class UserEditForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])

class ClassifyDisease(FlaskForm):
    pass