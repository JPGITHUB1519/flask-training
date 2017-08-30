from flask import render_template, flash, redirect, current_app
from . import main
from .. import db
from .forms import LoginForm
from ..emails import send_email

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

@main.route('/login', methods=['GET', 'POST'])
def login():
	form =  LoginForm()
	# returns false for get request, returns true when all data is correct
	if form.validate_on_submit():
		flash('Login Requested for username=%s' % (form.username.data))
		return redirect('/index')
	return render_template('login.html',
							title="Log In",
							form=form)

@main.route('/mail')
def send_mail():
	send_email('juanpedrotramposo@gmail.com', 'Welcome', 'mail', user="jean")
	send_email('juanpedrotramposo@gmail.com', 'Welcome', 'mail', user="jean")
	return "hey"