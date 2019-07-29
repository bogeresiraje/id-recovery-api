from main.app import db


# Pending account
class Pending(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(100))
	password = db.Column(db.String(100))
	code = db.Column(db.String(10))
	created_time = db.Column(db.DateTime)

	def __init__(self, *args, **kwargs):
		super(Pending, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Pending: %s>' % self.name


# User Account
class Account(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(100))
	phone = db.Column(db.String(20))
	password = db.Column(db.String(100))
	photo_name = db.Column(db.String(400), default='avatar.png')
	id_image_name = db.Column(db.String(400))
	created_time = db.Column(db.DateTime)

	def __init__(self, *args, **kwargs):
		super(Account, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Account: %s>' % self.name
