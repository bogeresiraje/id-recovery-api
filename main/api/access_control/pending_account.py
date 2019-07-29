import random
import datetime

from flask_mail import Message
from main.app import db, mail
from main.models import Pending, Account
from main.api.access_control.logger import Logger


class PendingAccount:
	def __init__(self, name, email, password):
		self.name = name
		self.email = email
		self.password = password

	# Check whether there is no other account that uses the same email
	def is_email_valid(self):
		return not bool(Account.query.filter(Account.email == self.email).first())

	# Send verification code to that email and save pending account to database
	def send_verification_code(self):
		code = str(random.randint(1000, 9999))
		message = Message('Verify Your ID Recovery Account With This Code',
				sender='ronniwallace2017@gmail.com', recipients=[self.email]
			)
		message.body = code
		mail.send(message)

		# Save pending account to database
		pending = Pending(name=self.name, email=self.email, password=self.password,
				created_time=datetime.datetime.now(), code = code
			)
		db.session.add(pending)
		db.session.commit()


class ConfirmAccount:
	def __init__(self, code):
		self.code = code

	# Check whether there exists a pending account with this code
	def is_code_correct(self):
		return bool(Pending.query.filter(Pending.code == self.code).first())

	# Check whether the code is still valid
	# If valid, continue to create account, otherwise delete that pending account
	# And maybe ask user to re-enter his credentials
	def is_code_valid(self):
		pending_account = Pending.query.filter(Pending.code == self.code).first()
		threshold = datetime.timedelta(seconds=300)
		return ( datetime.datetime.now() - pending_account.created_time ) < threshold

	# Delete pending account
	# Must be done when verification code has become invalid or when the
	# Normal account has been created from this pending account
	def delete_pending_account(self):
		pending_account = Pending.query.filter(Pending.code == self.code).first()
		db.session.delete(pending_account)
		db.session.commit()

	# Create new account
	def create_account(self):
		pending_account = Pending.query.filter(Pending.code == self.code).first()
		new_account = Account(name=pending_account.name, email=pending_account.email,
				password=pending_account.password
			)
		db.session.add(new_account)
		db.session.commit()

		# Delete this pending when normal account has been created
		self.delete_pending_account()

		# Login user
		logger = Logger(pending_account.email)
		logger.login_user()

		return new_account.email

