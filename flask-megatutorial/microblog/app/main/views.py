from flask import render_template, flash, redirect, current_app
from flask_login import login_required, current_user
from . import main
from .. import db
from .forms import LoginForm
from ..emails import send_email
from ..debugging import printd

@main.route('/')
@main.route('/index')
def index():
	# fake user
	user = {"nickname": "jean"}
	# fake posts
	posts = [
		{ 
			'author': {"nickname" : "Jhon"},
			'body': "Beautiful Day in Portland"
		},
		{
			'author': {"nickname": "Susan"},
			'body': "The avengers movie was so cool"
		}
	]
	
	return render_template('index.html', 
							user=user, 
							posts=posts)

@main.route('/tester')
def tester():
	return "Tester Route"
	
@main.route('/mail')
def send_mail():
	send_email('juanpedrotramposo@gmail.com', 'Welcome', 'mail', user="jean")
	send_email('juanpedrotramposo@gmail.com', 'Welcome', 'mail', user="jean")
	return "hey"

# protecting routes for authenticated users
@main.route('/secret')
@login_required
def secret():
	return 'Only authenticated users are allowed'