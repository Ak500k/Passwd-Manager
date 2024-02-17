from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from loginapp.models import User

email_validator = [DataRequired(), Email()]

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=email_validator)
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit_button = SubmitField('Register')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already exists in the database.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=email_validator)
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit_button = SubmitField('Login')

class AddPassword(FlaskForm):
    webaddress = StringField('Web Address', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=email_validator)
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField('Submit')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=email_validator)
    submit_button = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with this email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit_button = SubmitField('Reset Password')

class UserAccountUpdate(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=email_validator)
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit_button = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError('Email already exists in the database.')

class UpdatePassword(FlaskForm):
    webaddress = StringField('Web Address', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=email_validator)
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField('Update')
