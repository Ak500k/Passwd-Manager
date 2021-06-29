import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'  # for form in forms.py otherwise forms does not work
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # this line means where to create db

db = SQLAlchemy(app) # creating the instance of sqlalchemy as db
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'notification is-danger'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('DB_USER') # email id     Do this with environment variable
app.config['MAIL_PASSWORD'] = os.environ.get('DB_PASS') # password     Do this with environment variable
mail = Mail(app)

from loginapp import routes
