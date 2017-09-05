import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	"""
	Common Settings to all Configs
	"""
	SECRET_KEY = 'you-will-never-guess'
	# SECRET_KEY = os.environ.get('SECRET_KEY')

	# Flask-WTF 
	WTF_CSRF_ENABLED = True

	# custom mail settings
	FLASKY_MAIL_SUBJECT_PREFIX = '[FLASKY]'
	FLASKY_MAIL_SENDER = 'Flask Admin <juanpedrotramposo@gmail.com>'
	FLASKY_MAIL_TEMPLATES_FOLDER = '/mail'
	FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

	# disable notifications sqlalchemy
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True

	# Flask-SQLAlchemy path of the database
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')

	# mail
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	# never write your credentials in the scripts instead in environ variables
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or "juanpedrotramposo@gmail.com"
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or "23051519"

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-test.db')

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.db')

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}