from main.app import db
from main.models import Face, Account, Photo


class FaceDataHandler(object):
	@staticmethod
	def get_id_by_filename(filename):
		face_data = Face.query.filter(Face.data_name == filename).first()
		return face_data.id

	@staticmethod
	def update_data(email, identifier, photo_name, data_name):
		user = Account.query.filter(Account.email == email).first()
		photo = PhotoBag(identifier=identifier, photo_name=photo_name)
		face_data = FaceData(data_name=data_name)
		photo.photo_data.append(face_data)
		user.photos.append(photo)
		db.session.add_all([face_data, photo])
		db.session.commit()


	@staticmethod
	def get_user(label):
		img = FaceData.query.get(label)
		user = img.accounts[0]
		return user.id, user.email
