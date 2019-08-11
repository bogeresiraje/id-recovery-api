import os
import cv2

from main.app import app, db
from main.models import Account, FaceData
from main.api.handlers.count_handler import CountHandler


class UserHandler:
	@staticmethod
	def get_user(email):
		user_obj = Account.query.filter(Account.email == email).first()
		user = {}
		user.update(user_obj.__dict__)
		user.pop('_sa_instance_state', -1)
		return user

	@staticmethod
	def get_user_by_id(user_id):
		user = Account.query.get(user_id)
		return UserHandler().get_user(user.email)


	@staticmethod
	def update_data_set(email, data_set_name):
		user = Account.query.filter(Account.email == email).first()
		face_data = FaceData(data_name=data_set_name)
		db.session.add(face_data)
		user.data_sets.append(face_data)

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
	def change_id_photo(email, img):
		img_name = 'id_recov_' + str(CountHandler.get_count()) + '.jpg'
		filename = app.config['STATIC_DIR'] + '/' + img_name
		cv2.imwrite(filename, img)

		user = Account.query.filter(Account.email == email).first()
		user.id_image_name = img_name
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

	@staticmethod
	def search_owner(photo):
		user = Account.query.all()[0]
		return user.id

