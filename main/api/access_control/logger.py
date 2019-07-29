from flask import session
from main.models import Account


# Log in users by their email addresses
# Therefore, ( user ) implies ( email )
class Logger:
	def __init__(self, email):
		self.email = email

	def are_details_correct(self, password):
		return bool(Account.query.filter(Account.email == self.email, Account.password == password).first())

	def login_user(self):
		session[self.email] = True

	def logout_user(self):
		session.pop(self.email)

	def is_loggedin(self):
		try:
			session[self.email]
			return True

		except:
			return False