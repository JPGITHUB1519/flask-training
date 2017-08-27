import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Flask-WTF 
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# Flask-SQLAlchemy path of the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# folder where we will store the SQLAlchemy-migrate data files
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')