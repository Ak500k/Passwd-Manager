from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import validators
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from loginapp.models import User

class RegistrationForm(FlaskForm):
    """
    Registration form 
    Elements containing:
    1. name
    2. email
    3. password
    4. confirm password
    5. submit button
    """
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])

    submit_btn = SubmitField('Register')

    # Adding validation for abnormal anomalies
    def validate_email(self, email):
        test_condition = User.query.filter_by(email = email.data).first()
        if test_condition:
            raise ValidationError('Email already exist in database.')

class LoginForm(FlaskForm):    
    """
    Login form 
    Elements containing:
    1. email
    2. password
    3. submit button
    """
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit_btn = SubmitField('Login')


class AddPassword(FlaskForm):
    """ Form for add page. Where user will input therir credintial in password manager. """
    webaddress = StringField('Web Address', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit_btn = SubmitField('Submit')

# password reset form
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit_btn = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError('There is no account with this email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])

    submit_btn = SubmitField('Reset Password')


class UserAccountUpdate(FlaskForm):    
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit_btn = SubmitField('Update')

    # Adding validation for abnormal anomalies
    def validate_email(self, email):
        if email.data != current_user.email:
            test_condition = User.query.filter_by(email = email.data).first()
            if test_condition:
                raise ValidationError('Email already exist in database.')

class UpdatePassword(FlaskForm):
    """ Form for Update page. Where user will update their credintial in password manager. """
    webaddress = StringField('Web Address', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit_btn = SubmitField('Update')