import unittest
import time
from app import create_app, db
from app.models import User

class UserModelTestCase(unittest.TestCase):
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
		
	def test_password_setter(self):
		""" test password_hash is setted automatically"""
		u = User(password='cat')
		self.assertTrue(u.password_hash is not None)

	def test_no_password_getter(self):
		""" Test the password property is only read property """
		u = User(password='cat')
		with self.assertRaises(AttributeError):
			u.password

	def test_password_verification(self):
		u = User(password='cat')
		self.assertTrue(u.verify_password('cat'))
		self.assertFalse(u.verify_password('dog'))

	def test_password_salts_are_random(self):
		u = User(password='cat')
		u2 = User(password='cat')
		self.assertTrue(u.password_hash != u2.password_hash)

	# tests for token generators
	def test_valid_token_generation(self):
		""" Test the token is generated successfully
			Methods in test : generate_token, check_token
		"""
		u = User(nickname='jean', password='cat')
		# save the user in database to get the id
		db.session.add(u)
		db.session.commit()
		token = u.generate_token('tester_token_type')
		self.assertTrue(u.check_token(token))

	def test_expired_token_generation(self):
		""" Test the expiration time of a token """
		u = User(password='cat')
		db.session.add(u)
		db.session.commit()
		token = u.generate_token('tester_token_type', 1)
		time.sleep(2)
		self.assertFalse(u.check_token(token))

	# test individuals tokens
	def test_valid_confirmation_token(self):
		u = User(password='cat')
		db.session.add(u)
		db.session.commit()
		token = u.generate_confirmation_token()
		self.assertTrue(u.confirm(token))

	def test_invalid_confirmation_token(self):
		u1 = User(password='cat')
		u2 = User(password='dog')
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()
		token = u1.generate_confirmation_token()
		self.assertFalse(u2.confirm(token))

	def test_expired_confirmation_token(self):
		u = User(password='cat')
		db.session.add(u)
		db.session.commit()
		token = u.generate_confirmation_token(1)
		time.sleep(2)
		self.assertFalse(u.confirm(token))

	def test_valid_check_reset_password_token(self):
		u = User(password='cat')
		db.session.add(u)
		db.session.commit()
		token = u.generate_token('reset')
		self.assertTrue(u.check_reset_password_token(token))

	def test_invalid_check_reset_password_token(self):
		u1 = User(password='cat')
		u2 = User(password='perro')
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()
		token = u1.generate_token('reset')
		self.assertFalse(u2.check_reset_password_token(token))


