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


face_data = db.Table('account_face_data',
		db.Column('account_id', db.Integer, db.ForeignKey('account.id')),
		db.Column('face_data_id', db.Integer, db.ForeignKey('face_data.id'))
	)

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
	data_sets = db.relationship('FaceData', secondary=face_data,
			backref=db.backref('accounts', lazy='dynamic')
		)

	def __init__(self, *args, **kwargs):
		super(Account, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Account: %s>' % self.name


# Hols face data sets for users
class FaceData(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	data_name = db.Column(db.String(400))

	def __init__(self, *args, **kwargs):
		super(FaceData, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<FaceData: %s' % self.data_name


# Counter.
# This is used to main image names consistent and unique
class Counter(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	count = db.Column(db.Integer, unique=True)

	def __init__(self, *args, **kwargs):
		super(Counter, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Counter: %s' % str(self.count)
