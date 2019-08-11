import os
import sys
import cv2
import numpy as np
from werkzeug import secure_filename
from main.app import app, db
from main.api.handlers.count_handler import CountHandler
from main.api.handlers.user_handler import UserHandler
from main.api.handlers.face_data_handler import FaceDataHandler


class FaceRec(object):
	def __init__(self, email, photo):
		self.email = email
		self.photo = photo
		self.initialize()


	def initialize(self):
		# Initialize face and eye cascades
		face_cascade_path = os.path.join(
				app.config['CASCADES_DIR'], 'haarcascade_frontalface_default.xml'
			)
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
		self.img = img
		# Convert to grayscale
		gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		# Detect faces
		found, actual_faces = False, []
		faces = face_cascade.detectMultiScale(gray_img, 1.03, 2)
		for (x,y,w,h) in faces:
			# Check for eyes in the detected region.
			# This confirms that this is truly a face
			roi = gray_img[y:y+h, x:x+w]
			eyes = eye_cascade.detectMultiScale(roi, 1.03, 1)
			if len(eyes):
				# Face has been detected.
				# Save face data in the ( data_sets ) directory.
				# This will later be used for facial recoginition.
				# Resize to ( 200x200 ) pixels.
				face = cv2.resize(roi, (200, 200), interpolation=cv2.INTER_LINEAR)
				count = CountHandler.get_count()
				img_name = str(count) + '.pgm'
				file = app.config['DATA_SETS_DIR'] + '/bs/' + img_name
				actual_faces.append((file, img_name, face))
				found = True
		self.actual_faces = actual_faces
		return found, None


	# Save face train data, only called when user is also identified.
	def save_data(self, email):
		actual_faces = self.actual_faces.copy()
		for (file, img_name, face ) in actual_faces:
			cv2.imwrite(file, face)
			FaceDataHandler.update_data(email, img_name)


	def change_id_photo(self):
		self.save_data(self.email)
		img = self.img.copy()
		# Resize to ( 500x500 ) size
		img = cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA)
		return UserHandler.change_id_photo(self.email, img)


	def read_images(self, path, sz=None):
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
						raise

					except:
						print('Unexpected error: ', sys.exc_info()[0])
						raise
		return [x,y]


	def search_photo(self):
		owner_id = None
		[x,y] = self.read_images(app.config['DATA_SETS_DIR'])
		y = np.asarray(y, dtype=np.int32)

		model = cv2.face.EigenFaceRecognizer_create()
		model.train(np.asarray(x), np.asarray(y))
		for ( file, img_name, face ) in self.actual_faces:
			label, confidence = model.predict(face)
			print(confidence)
			if confidence <= 4500:
				owner_id, email = FaceDataHandler.get_user(label)
				self.save_data(email)
				break
		return owner_id
