from flask import render_template, flash, redirect
from flask_mail import Message
from app import app, mail
from .forms import LoginForm
from threading import Thread

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)

def send_email(to, subject, template, **kwargs):
	"""
	Send Asyncronous mail
	"""
	msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
				sender=app.config['FLASKY_MAIL_SENDER'],
				recipients=[to])
	msg.body = render_template(app.config['FLASKY_MAIL_TEMPLATES_FOLDER'] +  '/' + template + '.txt', **kwargs)
	msg.html = render_template(app.config['FLASKY_MAIL_TEMPLATES_FOLDER'] +  '/' + template + '.html', **kwargs) 	
	thr = Thread(target=send_async_email, args=[app, msg])
	thr.start()
	return thr

@app.route('/')
@app.route('/index')
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

@app.route('/tester')
def tester():
	return "Tester Route"

@app.route('/login', methods=['GET', 'POST'])
def login():
	form =  LoginForm()
	# returns false for get request, returns true when all data is correct
	if form.validate_on_submit():
		flash('Login Requested for username=%s' % (form.username.data))
		return redirect('/index')
	return render_template('login.html',
							title="Log In",
							form=form)

@app.route('/mail')
def send_mail():
	send_email('juanpedrotramposo@gmail.com', 'Welcome', 'mail', user="jean")
	send_email('juanpedrotramposo@gmail.com', 'Welcome', 'mail', user="jean")
	return "hey"