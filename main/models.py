import datetime
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


id_photos = db.Table('id_photos',
		db.Column('account_id', db.Integer, db.ForeignKey('account.id')),
		db.Column('photo_id', db.Integer, db.ForeignKey('photo.id'))
	)

# User Account
class Account(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(100))
	phone = db.Column(db.String(20))
	password = db.Column(db.String(100))
	photo_name = db.Column(db.String(400), default='avatar.png')
	created_time = db.Column(db.DateTime)
	id_photos = db.relationship('Photo', secondary=id_photos,
			backref=db.backref('users', lazy='dynamic')
		)

	def __init__(self, *args, **kwargs):
		super(Account, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Account: %s>' % self.name


faces = db.Table('photo_sets',
		db.Column('photo_id', db.Integer, db.ForeignKey('photo.id')),
		db.Column('face_id', db.Integer, db.ForeignKey('face.id'))
	)


# Keeps all id photos for a single user
class Photo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	identifier = db.Column(db.String(100))
	photo_name = db.Column(db.String(100))
	created_time = db.Column(db.DateTime, default=datetime.datetime.now)
	faces = db.relationship('Face', secondary=faces,
			backref=db.backref('photos', lazy='dynamic')
		)

	def __init__(self, *args, **kwargs):
		super(Photo, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Photo: %s>' % self.identifier



# Hols face data sets for users
class Face(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	data_name = db.Column(db.String(400))

	def __init__(self, *args, **kwargs):
		super(Face, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Face: %s' % self.data_name


# Counter.
# This is used to main image names consistent and unique
class Counter(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	count = db.Column(db.Integer, unique=True)

	def __init__(self, *args, **kwargs):
		super(Counter, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Counter: %s' % str(self.count)
