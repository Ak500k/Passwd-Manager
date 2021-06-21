from flask import render_template, flash, redirect, url_for, request
from loginapp import app, db, bcrypt, mail
from loginapp.forms import RegistrationForm, LoginForm, AddPassword, RequestResetForm, ResetPasswordForm
from loginapp.models import User, PasswordManager
from flask_login import login_user, current_user, logout_user, login_required # this line is important. Allows us to login the user.
from flask_mail import Message
"""
    File containes only routes
    Don't add any other things
"""

@app.route('/')
@app.route('/home')
def home():
    # home page code goes here.
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # below line does
    # if current user is logged in and user tries to go to register page it will redirect to home.
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # register page code goes here.
    page_title = 'Register'

    form = RegistrationForm()  # creating instance of Registration form from forms module

    # Adding validator for registration page
    # flash will return two objects. 1. message, 2. success status
    print(form.errors) # do not put this line on production app
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # creating hashed password
        
        user = User(name = form.name.data, 
                    email = form.email.data, 
                    password = hashed_password) # creating variable user and initilizing the values of name, email, password. Template -> models.py
        
        db.session.add(user) # adding user to table
        db.session.commit()  # commiting the table
        flash("Account Created. Now you can login.", 'success')
        return redirect(url_for('home'))

    return render_template('register.html', title=page_title, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # below line does
    # if current user is logged in and user tries to go to login page it will redirect to home.
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # login page code goes here.
    page_title = 'Login'

    form = LoginForm()  # creating instance of Login form from forms module

    # Adding validator for login page
    # flash will return two objects. 1. message, 2. success status
    print(form.errors)
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first() # checking if user input data is present in db.
                                                                   # If present then return the first query. Otherwise return none
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('manager'))
        else:
            flash('Email or password does not match.', 'danger')
    return render_template('login.html', title=page_title, form=form)





# password manager
# ISOLATE FROM OUTTER SHELL
@app.route('/manager')
@login_required
def manager():
    # print(current_user.id)
    # print(current_user.name)
    return render_template('manager.html', title='demo')

@app.route('/manager/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddPassword()
    
    print(form.errors) # do not put this line on production app
    if form.validate_on_submit():
        print(current_user.id)
        name = db.session.query(User).filter_by(id=current_user.id).first() # first creating the instence of user table then adding it to name
        field = PasswordManager(webaddress = form.webaddress.data, 
                                username = form.username.data, 
                                email = form.email.data, 
                                password = form.password.data, 
                                owner = name)

        db.session.add(field) # adding user to table
        db.session.commit()  # commiting the table
        flash("Field Added.", 'success')
        return redirect(url_for('manager'))
    return render_template('add.html', title='add-password', form=form)

@app.route('/manager/display', methods=['GET', 'POST'])
@login_required
def display():
    fields = db.session.query(PasswordManager).filter_by(owner_id=current_user.id).all()
    return render_template('display.html', title='dispaly', elements=fields)


# Code to loggout user from their account
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset REquest', sender='ashishdungdung6@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this request. No changes will be made.
'''
    mail.send(msg)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    # below line does
    # if current user is logged in and user tries to go to login page it will redirect to home.
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # login page code goes here.

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been set with instructions to reset you password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form = form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    # below line does
    # if current user is logged in and user tries to go to login page it will redirect to home.
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # login page code goes here.
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'danger')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # creating hashed password
        user.password = hashed_password
        db.session.commit()  # commiting the table
        flash("Your password has been updated. Now you can login.", 'success')
        return redirect(url_for('home'))
    return render_template('reset_token.html', title='Reset Password', form = form)