from flask_wtf import Form
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
	email = StringField('Email', validators=[Required(), Length(1, 120), Email()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')

class RegistrationForm(Form):
	email = StringField('Email', validators=[Required(), Length(1, 120), Email()])
	nickname = StringField('Username', validators=[Required(), Length(1,64), 
		Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, ''numbers, dots or underscores')])
	password = PasswordField('Password', validators=[Required(), EqualTo('password2', message="Password must match.")])
	password2 = PasswordField('Confirm Password', validators=[Required()])
	submit = SubmitField('Register')

	# customs validators
	# when we define validate_<name_of_field> we apply a new custom validator to that field
	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_nickname(self, field):
		if User.query.filter_by(nickname=field.data).first():
			raise ValidationError('Username already in use')

class UpdatePasswordForm(Form):
	old_password = PasswordField('Old Password', validators=[Required()])
	new_password = PasswordField('New password', validators=[Required()])
	submit = SubmitField('Save')

	def validate_old_password(self, field):
		if not current_user.verify_password(field.data):
			raise ValidationError('The Old Password you entered is not correct')

class ResetPasswordRequestForm(Form):
	email = StringField('Email', validators=[Required(), Length(1, 120), Email()])
	submit = SubmitField('Send')

	# we must not validate email here to avoid brute force attacks
	# def validate_email(self, field):
	# 	if not User.query.filter_by(email=field.data).first():
	# 		raise ValidationError('This email does not exists')

class ResetPasswordForm(Form):
	new_password = PasswordField('New password', validators=[Required()])
	submit = SubmitField('Save')
