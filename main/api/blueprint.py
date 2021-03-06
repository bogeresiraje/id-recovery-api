from flask import Blueprint, request, jsonify
from main.api.access_control.pending_account import *
from main.api.handlers.user_handler import UserHandler
from main.api.face.face_rec import FaceRec


api = Blueprint('api', __name__, static_folder='uploads')


@api.route('/')
def index():
	return 'id recovery app'


# Accept user credentials to create account
@api.route('/create_account', methods=['GET', 'POST'])
def create_account():
	if request.method == 'POST':
		name, email = request.form['name'], request.form['email']
		password = request.form['password']

		# Create an instance of a pending account
		pending = PendingAccount(name=name, email=email, password=password)

		# If email is valid continue to save the pending account to the database
		# and send the verification code
		# Otherwise, notify the user that email is invalid
		if pending.is_email_valid():
			pending.send_verification_code()
			return jsonify({ 'verification_code_sent': True })

		else:
			return jsonify({ 'invalid_email': True })

	else:
		return jsonify({ 'fail': True })


# Confirm email using the verfication code and create the account
@api.route('/confirm_verification_code', methods=['GET', 'POST'])
def confirm_verfication_code():
	if request.method == 'POST':
		code = request.form['code']

		confirm_account = ConfirmAccount(code)
		# If code is correct, continue to check whether it is still valid
		# Otherwise, notify the user that a wrong code was submitted
		if confirm_account.is_code_correct():
			# If code is invalid, notify the user
			# Otherwise notify the user
			if confirm_account.is_code_valid():
				# Create new account
				email = confirm_account.create_account()
				return jsonify({ 'email': email })

			else:
				confirm_account.delete_pending_account()
				return jsonify({ 'invalid_code': True })

		else:
			return jsonify({ 'wrong_code': True })

	else:
		return jsonify({ 'fail': True })


# Login user
@api.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email, password = request.form['email'], request.form['password']
		logger = Logger(email)
		if logger.are_details_correct(password):
			logger.login_user()
			return jsonify({ 'email': email })

		else:
			return jsonify({ 'wrong_details': True })

	else:
		return jsonify({ 'fail': True })


# Logout user
@api.route('/logout', methods=['GET', 'POST'])
def logout():
	if request.method == 'POST':
		email = request.form['email']
		logger = Logger(email)
		logger.logout_user()
		return jsonify({ 'success': True })

	else:
		return jsonify({ 'fail': True })


# Return user
@api.route('/get_user', methods=['GET', 'POST'])
def get_user():
	if request.method == 'POST':
		email = request.form['email']
		user = UserHandler().get_user(email)
		return jsonify({ 'user': user })

	else :
		return jsonify({ 'fail': True })


# Return user
@api.route('/get_user_by_id', methods=['GET', 'POST'])
def get_user_by_id():
	if request.method == 'POST':
		user_id = request.form['user_id']
		user = UserHandler().get_user_by_id(user_id)
		return jsonify({ 'user': user })

	else :
		return jsonify({ 'fail': True })



# Change profile photo
@api.route('/change_profile_photo', methods=['GET', 'POST'])
def change_profile_photo():
	if request.method == 'POST':
		email = request.form['email']
		photo = request.files['photo']
		user = UserHandler().change_profile_photo(email, photo)
		return jsonify({ 'user': user })

	else:
		return jsonify({ 'fail': True })


# Add id photo
@api.route('/add_id_photo', methods=['GET', 'POST'])
def add_id_photo():
	if request.method == 'POST':
		email, identifier = request.form['email'], request.form['identifier']
		photo = request.files['photo']
		face_rec = FaceRec(email, photo)
		if face_rec.detect_face()[0]:
			user_id = face_rec.add_id_photo(identifier)
			return jsonify({ 'user_id': user_id })
		else:
			return jsonify({ 'no_face_detected': True })

	else:
		return jsonify({ 'fail': True })


# Delete ID photo
@api.route('/delete_id', methods=['GET', 'POST'])
def delete_id():
	if request.method == 'POST':
		photo_id = request.form['photo_id']
		UserHandler.delete_id(photo_id)
		return jsonify(({ 'photo_id': int(photo_id) }))
	else:
		return jsonify({ 'fail': True })


# Edit user name
@api.route('/edit_name', methods=['GET', 'POST'])
def edit_name():
	if request.method == 'POST':
		email, name = request.form['email'], request.form['name']
		user = UserHandler().edit_user_name(email, name);
		return jsonify({ 'user': user })

	else:
		return jsonify({ 'fail': True })


# Edit user phone
@api.route('/edit_phone', methods=['GET', 'POST'])
def edit_phone():
	if request.method == 'POST':
		email, phone = request.form['email'], request.form['phone']
		user = UserHandler().edit_user_phone(email, phone);
		return jsonify({ 'user': user })

	else:
		return jsonify({ 'fail': True })


# Search For Owner
@api.route('/search_owner', methods=['GET', 'POST'])
def search_owner():
	if request.method == 'POST':
		photo = request.files['photo']
		face_rec = FaceRec(None, photo)
		found, faces = face_rec.detect_face()
		if found:
			user = face_rec.search_photo()
			if user:
				return jsonify({ 'user': user })
			return jsonify({ 'no_owner_found': True })
		return jsonify({ 'no_face_detected': True })

	else:
		return jsonify({ 'fail': True })


# View all photos
@api.route('/view_all', methods=['GET', 'POST'])
def view_all():
	if request.method == 'POST':
		user_id = request.form['user_id']
		photos = list(UserHandler.get_all_photos(user_id))
		return jsonify({ 'photos': photos })
	else:
		return jsonify({ 'fail': True })


# For deleting account.
@api.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
	if request.method == 'POST':
		user_id = request.form['user_id']
		UserHandler.delete_account(user_id)
		return jsonify({ 'success': True })
	else:
		return jsonify({ 'fail': True })
