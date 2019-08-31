import os
import cv2

from main.app import app, db
from main.models import Account, Face, Photo
from main.api.handlers.count_handler import CountHandler


class UserHandler:
	@staticmethod
	def get_user(email):
		user_obj = Account.query.filter(Account.email == email).first()
		id_photos = user_obj.id_photos
		user = {}
		user.update(user_obj.__dict__)
		user.pop('_sa_instance_state', -1)
		user.pop('id_photos', -1)

		photos = []
		for _p in id_photos:
			photos.append(UserHandler.get_id_photo(_p.id))

		user['photos'] = photos
		return user

	@staticmethod
	def get_user_by_id(user_id):
		user = Account.query.get(user_id)
		return UserHandler().get_user(user.email)


	@staticmethod
	def get_id_photo(photo_id):
		_p = Photo.query.get(photo_id)
		photo = {}
		photo.update(_p.__dict__)
		photo.pop('_sa_instance_state', -1)
		return photo

	@staticmethod
	def delete_id(photo_id):
		photo = Photo.query.get(photo_id)
		# Get all faces attached to this ID photo
		faces = photo.faces
		# Delete every face from the database and the file in local storage
		for face in faces:
			filename = face.data_name
			file_dir = os.path.join(app.config['DATA_SETS_DIR'], filename)
			if os.path.exists(file_dir):
				os.remove(file_dir)
			db.session.delete(face)

		# Then delete the photo itself
		photo_name = photo.photo_name
		photo_dir = os.path.join(app.config['STATIC_DIR'], photo_name)
		if os.path.exists(photo_dir):
			os.remove(photo_dir)
		db.session.delete(photo)
		db.session.commit()


	@staticmethod
	def get_all_photos(user_id):
		user = Account.query.get(user_id)
		for photo in user.id_photos:
			yield UserHandler.get_id_photo(photo.id)


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
		# Delete current profile pic to free up space
		curr_photo_dir = app.config['STATIC_DIR'] + '/' + user.photo_name
		if(os.path.exists(curr_photo_dir)):
			os.remove(curr_photo_dir)

		user.photo_name = photo_name
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

	@staticmethod
	def delete_account(user_id):
		user = Account.query.get(user_id)
		# Clear all your user data and images stored on storage
		id_dir = app.config['STATIC_DIR'] + '/' + user.id_image_name
		photo_dir = app.config['STATIC_DIR'] + '/' + user.photo_name
		# Id ID exists, delete
		if os.path.exists(id_dir):
			os.remove(id_dir)

		# If profile pic exists, and it's not the default avatar, delete
		if user.photo_name is not 'avatar.png':
			if os.path.exists(photo_dir):
				os.remove(photo_dir)

		# Delete all face data sets of this user.
		data_sets = user.data_sets
		for data_set in data_sets:
			data_set_dir = app.config['DATA_SETS_DIR'] + '/bs/' + data_set.data_name
			# Then delete the file and the data set
			if os.path.exists(data_set_dir):
				os.remove(data_set_dir)
				db.session.delete(data_set)

		db.session.delete(user)
		db.session.commit()

