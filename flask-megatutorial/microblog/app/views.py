from flask import render_template
from app import app

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
