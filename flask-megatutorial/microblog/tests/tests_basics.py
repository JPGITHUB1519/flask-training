import unittest
from flask import current_app
from app import create_app, db

class BasicTestCase(unittest.TestCase):
	def setUp(self):
		"""
		Create application for testing and activates its context
		"""
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()

	def tearDown(self):
		"""
		Remove application context and database
		"""
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	# methods that begins with test_ are executed 	
	def test_app_exists(self):
		"""
		Ensure that application instance exists
		"""
		self.assertFalse(current_app is None)

	def test_app_is_testing(self):
		"""
		Ensure the app is running is under the testing configuration
		"""
		self.assertTrue(current_app.config['TESTING'])



