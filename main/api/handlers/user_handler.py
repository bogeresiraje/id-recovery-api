import os
from main.app import app, db
from main.models import Account


class UserHandler:
	@staticmethod
	def get_user(email):
		user_obj = Account.query.filter(Account.email == email).first()
		user = {}
		user.update(user_obj.__dict__)
		user.pop('_sa_instance_state', -1)
		return user

	@staticmethod
	def change_profile_photo(email, photo):
		photo_name = photo.filename
		photo_file = os.path.join(app.config['STATIC_DIR'], photo_name)
		photo.save(photo_file)

		user = Account.query.filter(Account.email == email).first()
		user.photo_name = photo_name
		db.session.commit()

		return UserHandler().get_user(user.email)

	@staticmethod
	def change_id_photo(email, photo):
		photo_name = photo.filename
		photo_file = os.path.join(app.config['STATIC_DIR'], photo_name)
		photo.save(photo_file)

		user = Account.query.filter(Account.email == email).first()
		user.id_image_name = photo_name
		db.session.commit()

		return UserHandler().get_user(user.email)

	@staticmethod
	def edit_user_name(email, name):
		user = Account.query.filter(Account.email == email).first()
		user.name = name
		db.session.commit()
		return UserHandler().get_user(user.email)

	@staticmethod
	def edit_user_phone(email, phone):
		user = Account.query.filter(Account.email == email).first()
		user.phone = phone
		db.session.commit()
		return UserHandler().get_user(user.email)

