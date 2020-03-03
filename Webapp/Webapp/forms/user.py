"""
Hanwei Wang
Time: 29-2-2020 12:36
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
    # in English is the comments
    # 中文的话是需要特别注意的地方以及需要检查的地方
"""

from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, ValidationError, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from Webapp.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo(password)])
    email = StringField('Email', validators= [DataRequired(), Email()])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('The username is already in use, please take another one!')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('The email is already in use, please take another one!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=30)])
    new_email = StringField('New Email', validators=[DataRequired(), Email()])
    new_email_again = StringField('New Email repeat', validators=[DataRequired(), EqualTo(new_email)])
    submit = SubmitField('Update')



