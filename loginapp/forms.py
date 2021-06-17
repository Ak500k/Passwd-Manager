from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
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
    """ Form for add page. Where user will input therir credintial in password generator. """
    webaddress = StringField('Web Address', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit_btn = SubmitField('Submit')