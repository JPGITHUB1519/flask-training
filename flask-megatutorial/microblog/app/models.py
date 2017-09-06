from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from app import db
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        """ Set the user role. if the user emails is equals to admin, his role will be admin else default """
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email ==     current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return '<User %r>' % (self.nickname)

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

    def can(self, permissions):
        """ Performs a bitwise and operation between the requested permissions and the permissions of the assigned role.
        The method returns True if all the requested bits are present in the role, which means that the user should be
        allowed to perform the task.
        """
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)


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

class AnonymousUser(AnonymousUserMixin):
    """ Assigned to current user when there is not logged users """
    def can(self, permissions):
        return False

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

login_manager.anonymous_user = AnonymousUser

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % (self.name)

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                    Permission.COMMENT |
                    Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                    Permission.COMMENT |
                    Permission.WRITE_ARTICLES |
                    Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


