from app import app

@app.route('/')
@app.route('/index')
def index():
	return "Hello World"

@app.route('/tester')
def tester():
	return "Tester Route"
