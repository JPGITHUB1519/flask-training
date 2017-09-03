""" This file is used to execute code from shell """
u = User.query.first()
token = u.generate_token('confirmation')
print u.reset_password(token)