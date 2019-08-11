from main.app import db
from main.models import FaceData, Account


class FaceDataHandler(object):
	@staticmethod
	def get_id_by_filename(filename):
		face_data = FaceData.query.filter(FaceData.data_name == filename).first()
		return face_data.id

	@staticmethod
	def update_data(email, data_name):
		user = Account.query.filter(Account.email == email).first()
		face_data = FaceData(data_name=data_name)
		db.session.add(face_data)
		user.data_sets.append(face_data)
		db.session.commit()


	@staticmethod
	def get_user(label):
		img = FaceData.query.get(label)
		user = img.accounts[0]
		return user.id, user.email
