import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Flask-WTF 
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# Flask-SQLAlchemy path of the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

# mail
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
# never write your credentials in the scripts instead in environment variables
# MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
# MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_USERNAME = "juanpedrotramposo@gmail.com"
MAIL_PASSWORD = "23051519"
# custom mail settings
FLASKY_MAIL_SUBJECT_PREFIX = '[FLASKY]'
FLASKY_MAIL_SENDER = 'Flask Admin <juanpedrotramposo@gmail.com>'
FLASKY_MAIL_TEMPLATES_FOLDER = '/mail'

