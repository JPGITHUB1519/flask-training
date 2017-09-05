from flask import render_template, redirect, request, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm, UpdatePasswordForm, ResetPasswordRequestForm, ResetPasswordForm
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
		flash('Invalid Username or Password', 'danger')

	# when get shows the template
	return render_template('/auth/login.html', form=form) 	

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out', 'success')
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
	return render_template('auth/unconfirmed.html', user=current_user)

@auth.route('/confirm')
def resend_confirmation():
	token =  current_user.generate_confirmation_token()
	send_email(current_user.email, 'Confirm your account', 'auth/email/confirm', user=current_user, token=token)
	flash('A new confirmation email has been sent to you by email', "success")
	return redirect(url_for('main.index')),

@auth.route('/update-password', methods=['GET', 'POST'])
def update_password():
	form = UpdatePasswordForm()
	if form.validate_on_submit():
		current_user.password = form.new_password.data
		db.session.add(current_user)
		db.session.commit()
		flash('Your Password was updated correctly', "success")
		return redirect(url_for('main.index'))

	return render_template('/auth/update_password.html', form=form)

@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		token = user.generate_token('reset')
		send_email(user.email, 'Reset Your password', 'auth/email/reset', user=user, token=token)
		flash('A reset password link has been set to you by email', 'info')
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password_request.html', form=form)

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	user = User.query.filter_by(email=request.args.get('email')).first()
	if user:
		if user.check_reset_password_token(token):
			form = ResetPasswordForm()
			if form.validate_on_submit():
				user.password = form.new_password.data
				db.session.add(user)
				db.session.commit()
				flash('Your password was updated correctly', 'success')
				return redirect(url_for('auth.login'))
			return render_template('auth/reset_password.html', user=user, form=form)
	flash('The reset link in invalid or has expired', 'danger')
	return redirect(url_for('auth.login'))