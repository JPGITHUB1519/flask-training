from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm
from .. import db
from ..emails import send_email
from ..debugging import printd


# handling unconfirmed users
# auth.before_app_request works in the whole aplication, auth.before_request only works for the current blueprint
@auth.before_app_request
def before_request():
	if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5] != 'auth.':
		return redirect(url_for('auth.unconfirmed'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	# when post validate the form
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid Username or Password')

	# when get shows the template
	return render_template('/auth/login.html', form=form) 	

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out')
	return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,	
					nickname=form.nickname.data,
					password=form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email(user.email, 'Confirm your account', '/auth/email/confirm', user=user, token=token)
		flash('A confirmation email has been sent to you by email')
		# login user after register
		login_user(user)
		return redirect(url_for('main.index'))

	return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash('You have confirmed your account, Thanks!')
	else:
		flash('The confirmation link in invalid or has expired')

	return redirect(url_for('main.index'))

@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect('main.index')
	return render_template('auth/unconfirmed.html')