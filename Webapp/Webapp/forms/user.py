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
from wtforms import StringField, SubmitField, ValidationError, BooleanField, PasswordField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, Length, EqualTo
from Webapp.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 12)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 30)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
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

class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=12)])
    new_email = StringField('New Email', validators=[DataRequired(), Email()])
    new_email_again = StringField('Confirm The New Email ', validators=[DataRequired(), EqualTo('new_email')]) # equal to need the name of the var, in string format
    submit = SubmitField('Update profile')

    # The function named as validate_*** in form class will be called when this form class be validated_on_submit
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('The username is already in use, please take another one!')

    def validate_email(self, new_email):
        user = User.query.filter_by(email = new_email.data).first()
        if user:
            raise ValidationError('The email is already in use, please take another one!')

class UpdatePasswordForm(FlaskForm):
    old_password = StringField('Old Password', validators=[DataRequired(), Length(min=1, max=12)])
    new_password = StringField('New Password', validators=[DataRequired(), Length(min=8, max=30)])
    new_password_again = StringField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')]) # equal to need the name of the var, in string format
    submit = SubmitField('Change password')

class UpdateProfilePicForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Change profile picture')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')














