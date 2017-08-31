from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_login import LoginManager
#from flask.ext.bootstrap import Bootstrap
from config import config

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
bootstrap = Bootstrap()
# keep track of the user ips and browser and logs user
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
#bootstrap = Bootstrap()

def create_app(config_name):
	""" Factory Function to create app"""
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	db.init_app(app)
	bootstrap.init_app(app)
	mail.init_app(app)
	login_manager.init_app(app)

	# main blueprint
	from main import main as main_blueprint
	from .auth import auth as auth_blueprint
	app.register_blueprint(main_blueprint)
	app.register_blueprint(auth_blueprint, url_prefix='/auth')

	return app