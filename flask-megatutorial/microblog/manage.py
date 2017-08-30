#!vflask/bin/python
import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import User

app = os.getenv('FLASK_CONFIG') or create_app('default')

migrate = Migrate(app, db)
manager = Manager(app)

def make_shell_context():
	return dict(app=app, db=db, User=User)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test():
	"""
	Run the Units Tests
	"""
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
	manager.run()