from sqlalchemy.orm import backref
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from loginapp import db, login_manager, app
from flask_login import UserMixin # this line is also important dono why


# below is the login manager loader 
# this line is important. Don't know what it does. 
# There in documentation @ https://flask-login.readthedocs.io/en/latest/
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)
    
    passwords = db.relationship('PasswordManager', backref='owner') # adding realtionship bertween user table and password manager table.

    # To reset password
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    ############################
    def __repr__(self):
        return f"User {self.name}, {self.email}, {self.password} " 

class PasswordManager(db.Model):
    __tablename__ = 'password_manager'
    sl = db.Column(db.Integer, primary_key = True)
    webaddress = db.Column(db.String(100), nullable = False)
    username = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(120), nullable = False)
    password = db.Column(db.String(60), nullable = False)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"User {self.sl}: {self.webaddress}, {self.username}, {self.email}, {self.password} "

