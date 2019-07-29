import os


class Configuration(object):
	APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345@localhost:5432/id_recovery'
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	STATIC_DIR = os.path.join(APPLICATION_DIR, 'api/uploads')
	SECRET_KEY = 'hgdfydUH#&SF@Fhytdt5785'
	DEBUG = True

	# Mail configs
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USERNAME = 'ronniwallace2017@gmail.com'
	MAIL_PASSWORD = 'wilishere06'
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True