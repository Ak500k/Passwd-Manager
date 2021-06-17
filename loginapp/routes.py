from flask import render_template, flash, redirect, url_for
from loginapp import app, db, bcrypt
from loginapp.forms import RegistrationForm, LoginForm, AddPassword
from loginapp.models import User, PasswordManager
from flask_login import login_user # this line is important. Allows us to login the user.

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
    # register page code goes here.
    page_title = 'Register'

    form = RegistrationForm()  # creating instance of Registration form from forms module

    # Adding validator for registration page
    # flash will return two objects. 1. message, 2. success status
    print(form.errors) # do not put this line on production app
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # creating hashed password
        user = User(name = form.name.data, email = form.email.data, password = hashed_password) # creating variable user and initilizing the values of name, email, password. Template -> models.py
        db.session.add(user) # adding user to table
        db.session.commit()  # commiting the table
        flash("Account Created. Now you can login.", 'success')
        return redirect(url_for('home'))

    return render_template('register.html', title=page_title, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
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
            return redirect(url_for('manager'))
        else:
            flash('Email or password does not match.', 'danger')
    return render_template('login.html', title=page_title, form=form)





# password manager
# ISOLATE FROM OUTTER SHELL
@app.route('/manager')
def manager():
    return render_template('manager.html', title='demo')

@app.route('/manager/add', methods=['GET', 'POST'])
def add():
    form = AddPassword()

    print(form.errors) # do not put this line on production app
    if form.validate_on_submit():
        field = PasswordManager(webaddress = form.webaddress.data, username = form.username.data, 
        email = form.email.data, password = form.password.data)
        db.session.add(field) # adding user to table
        db.session.commit()  # commiting the table
        flash("Field Added.", 'success')
        return redirect(url_for('manager'))
    return render_template('add.html', title='add-password', form=form)

@app.route('/manager/display')
def display():
    return render_template('display.html', title='dispaly')