import os



# # dev config
# class Configuration(object):
# 	APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
# 	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345@localhost:5432/id_recovery'
# 	SQLALCHEMY_TRACK_MODIFICATIONS = True
# 	STATIC_DIR = os.path.join(APPLICATION_DIR, 'api/uploads')
# 	# Path for remporary images -> for face detection
# 	TEMP_IMAGES = os.path.join(APPLICATION_DIR, 'api/face/temp_images')
# 	# Path forOpenCV haar cascades
# 	CASCADES_DIR = os.path.join(APPLICATION_DIR, 'api/face/cascades')
# 	# Path for data sets.
# 	DATA_SETS_DIR = os.path.join(APPLICATION_DIR, 'api/face/data_sets')
# 	SECRET_KEY = 'hgdfydUH#&SF@Fhytdt5785'
# 	DEBUG = True

# 	# Mail configs
# 	MAIL_SERVER = 'smtp.gmail.com'
# 	MAIL_PORT = 465
# 	MAIL_USERNAME = 'ronniwallace2017@gmail.com'
# 	MAIL_PASSWORD = 'wilishere06'
# 	MAIL_USE_TLS = False
# 	MAIL_USE_SSL = True



# prod config
class Configuration(object):
	APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
	SQLALCHEMY_DATABASE_URI = 'postgres://xcmtwtuzteggyo:51c2a3b9dd5708598b569ba82192da488639800ed6a6100b824b22c69c0bbe3d@ec2-23-21-148-223.compute-1.amazonaws.com:5432/dfet9ct7nt30sn'
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	STATIC_DIR = os.path.join(APPLICATION_DIR, 'api/uploads')
	# Path for remporary images -> for face detection
	TEMP_IMAGES = os.path.join(APPLICATION_DIR, 'api/face/temp_images')
 	# Path forOpenCV haar cascades
 	CASCADES_DIR = os.path.join(APPLICATION_DIR, 'api/face/cascades')
	# Path for data sets.
	DATA_SETS_DIR = os.path.join(APPLICATION_DIR, 'api/face/data_sets')
	SECRET_KEY = 'hgdfydUH#&SF@Fhytdt5785'
	DEBUG = True

	# Mail configs
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USERNAME = 'ronniwallace2017@gmail.com'
	MAIL_PASSWORD = 'wilishere06'
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True
