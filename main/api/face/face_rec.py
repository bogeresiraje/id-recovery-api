import os
import sys
import cv2
import numpy as np
from werkzeug import secure_filename
from main.models import Account, Photo, Face
from main.app import app, db
from main.api.handlers.count_handler import CountHandler
from main.api.handlers.user_handler import UserHandler
from main.api.handlers.face_data_handler import FaceDataHandler


def write_face(face):
	pass


def write_photo(photo):
	pass


class FaceRec(object):
	def __init__(self, email, photo):
		self.email = email
		self.photo = photo
		self.initialize()


	def initialize(self):
		# Initialize face and eye cascades

		# Pre-trained model for face detection
		face_cascade_path = os.path.join(
				app.config['CASCADES_DIR'], 'haarcascade_frontalface_default.xml'
			)
		# Pre-trained model for eye detection
		eye_cascade_path = os.path.join(
				app.config['CASCADES_DIR'], 'haarcascade_eye.xml'
			)

		face_cascade = cv2.CascadeClassifier(face_cascade_path)
		eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
		self.face_cascade, self.eye_cascade = face_cascade, eye_cascade


	def detect_face(self):
		# Localize the necessary objects
		face_cascade, eye_cascade = self.face_cascade, self.eye_cascade
		photo = self.photo

		# Save the image temporarily in ( temp_images ) directory
		# This is where OpenCV will read the image from
		filename = secure_filename(photo.filename)
		file = os.path.join(app.config['TEMP_IMAGES'], filename)
		photo.save(file)

		# Read temporary image
		img = cv2.imread(file)
		# Reshape to (400, 400)
		img = cv2.resize(img, (1000, 1000), interpolation=cv2.INTER_AREA)
		self.img = img
		# Convert to grayscale
		gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		# Delete temporary image
		if os.path.exists(file):
			os.remove(file)
		else:
			print(file, 'does not exist')
			pass

		# Detect faces
		found, actual_faces = False, []
		faces = face_cascade.detectMultiScale(gray_img, 1.03, 5)
		for (x,y,w,h) in faces:
			# Check for eyes in the detected region.
			# This confirms that this is truly a face
			roi = gray_img[y:y+h, x:x+w]
			eyes = eye_cascade.detectMultiScale(roi, 1.03, 5)
			if len(eyes):
				# Face has been detected.
				# Resize to ( 400x400 ) pixels.
				face = cv2.resize(roi, (200, 200), interpolation=cv2.INTER_LINEAR)
				count = CountHandler.get_count()
				img_name = str(count) + '.pgm'

				# Check if data sets dir ( path ) exists
				path =  app.config['DATA_SETS_DIR'] + '/bs/'
				if os.path.exists(path):
					pass
				else:
					path = os.path.join(os.path.config['APPLICATION_DIR'], 'api/face/data_sets/bs')
					os.mkdir(path)

				file = path + img_name
				actual_faces.append((file, img_name, face))
				found = True

		self.actual_faces = actual_faces
		return found, None


	# Save face train data, only called when user is also identified.
	def save_data(self, email, identifier):
		actual_faces = self.actual_faces.copy()
		# Photo obj
		photo_name = 'id_recov_' + str(CountHandler.get_count()) + '.jpg'
		filename = app.config['STATIC_DIR'] + '/' + photo_name
		cv2.imwrite(filename, self.img)

		photo = Photo(identifier=identifier, photo_name=photo_name)
		# User obj
		user = Account.query.filter(Account.email == email).first()
		for (file, img_name, face ) in actual_faces:
			cv2.imwrite(file, face)
			# Face object
			face = Face(data_name=img_name)
			photo.faces.append(face)
			db.session.add(face)

		user.id_photos.append(photo)
		db.session.add(photo)
		db.session.commit()
		return user.id


	def add_id_photo(self, identifier):
		return self.save_data(self.email, identifier)


	def read_images(self, path, sz=None):
		# Check if path exists
		if os.path.exists(path):
			pass
		else:
			_dir = os.path.join(os.path.config['APPLICATION_DIR'], 'api/face/data_sets/bs')
			os.mkdir(_dir)

		x, y = [], []
		for dirname, dirnames, filenames in os.walk(path):
			for subdirname in dirnames:
				subject_path = os.path.join(dirname, subdirname)
				for filename in os.listdir(subject_path):
					try:
						if filename == '.directory':
							continue
						img = cv2.imread(os.path.join(subject_path, filename), cv2.IMREAD_GRAYSCALE)
						# Resize to given size if given
						if sz is not None:
							cv2.resize(img, (200, 200))
						x.append(np.asarray(img, dtype=np.uint8))
						image_id = FaceDataHandler.get_id_by_filename(filename)
						y.append(image_id)

					except IOError:
						print('IO Error({0}): {1}'.format(
								IOError.errno, IOError.strerror
							))

					except:
						print('Unexpected error: ', sys.exc_info()[0])
						
		return [x,y]


	def search_photo(self):
		owner_id = None
		[x,y] = self.read_images(app.config['DATA_SETS_DIR'])
		y = np.asarray(y, dtype=np.int32)

		# Initialize EigenFace face recognizer
		model = cv2.face.EigenFaceRecognizer_create()
		# Train the face recognition model with sample images
		model.train(np.asarray(x), np.asarray(y))
		for ( file, img_name, face ) in self.actual_faces:
			label, confidence = model.predict(face)
			print(confidence)
			if confidence <= 4000:
				face = Face.query.get(label)
				id_photo = face.photos[0]
				_u = id_photo.users[0]
				user = {}
				user.update(_u.__dict__)
				user.pop('_sa_instance_state', -1)
				user['found_id_photo'] = id_photo.photo_name
				user['found_id_name'] = id_photo.identifier
				return user
