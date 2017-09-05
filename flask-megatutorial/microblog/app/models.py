from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from app import db
from . import login_manager

class User(UserMixin, db.Model):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    # read only property password
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # automatically set password hast after setting password property
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

    # user validations methods
    def generate_confirmation_token(self, expiration=3600):
        """ Generate a new encrypted confirmation token"""
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm' : self.id})

    # todo - refactor this using dinamically token generations
    def confirm(self, token):
        """ Confirm user token to activate user"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception as e:
            return False

        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def check_reset_password_token(self, token):
        """ Checks if a valid reset token """
        data = self.check_token(token)
        if data.get('reset') != self.id:
            return False
        return True

    # token generation methods
    def generate_token(self, token_type, expiration=3600):
        """ Refactor - Generate a new encrypted confirmation token
        
        Returns:
            @string - Returns the generated token
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({token_type : self.id})

    def check_token(self, token):
        """ Check if X token is valid. 
        
        Returns:
            if the token is valid:
                @dict - data of the token
            else:
                @boolean - false 
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception as e:
            return False
        return data



class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
