from flask import render_template, redirect, request, url_for, session, flash
from data.model import User, Post, save_user, post_image
# from data.model_modules import unserialize_models, get_prediction
from data.model_modules import get_cropped_face
from data.modules import not_logged_in, is_logged_in, get_signin_details, exception_error, check_password, get_signup_details, \
    get_passwords, get_emails, base_encode_image, api_identification
from werkzeug.datastructures import FileStorage
from data import app, db
import base64
import io


# age_model, gender_model, age_class_model = unserialize_models()


@app.route('/', methods=['GET', 'POST'])
def index():
    resp = is_logged_in(session)
    if resp:
        return resp
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    resp = is_logged_in(session)
    if resp:
        return resp
    if request.method == 'GET':
        return render_template('signin.html')
    try:
        username, password = get_signin_details(request.form)
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user'] = user.to_dict()
            flash('Signed in Successfully', 'success')
            return redirect(url_for('home'))
        flash('Wrong Credentials', 'danger')
        return redirect(url_for('login'))
    except Exception as e:
        return exception_error(e, 'login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    resp = is_logged_in(session)
    if resp:
        return resp
    if request.method == 'GET':
        return render_template('signup.html')
    try:
        name, username, email, password = get_signup_details(request.form)
        if check_password(password) is None:
            flash('Weak Password', 'danger')
            return redirect(url_for('register'))
        if len(User.query.filter_by(username=username).all()) != 0:
            flash('User Already Exist', 'danger')
            return redirect(url_for('register'))
        if len(User.query.filter_by(email=email).all()) != 0:
            flash('Email Already Used', 'danger')
            return redirect(url_for('register'))
        save_user(username=username, name=name, email=email, password=password)
        flash('New User Saved Successfully', 'success')
        return redirect(url_for('login'))
    except Exception as e:
        return exception_error(e, 'register')


@app.route('/home', methods=['GET', 'POST'])
def home():
    resp = not_logged_in(session)
    if resp:
        return resp
    return render_template('homepage.html')


@app.route('/scan', methods=['GET'])
def scan():
    resp = not_logged_in(session)
    if resp:
        return resp
    return render_template('scan.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        try:
            # 1️⃣ Check for uploaded file
            file = request.files.get('file')
            webcam_data = request.form.get('image')  # base64 from hidden input

            if file and file.filename != "":
                # File Upload Flow
                image_bytes = file.read()
                if not image_bytes:
                    flash('Uploaded file contained no data.', 'danger')
                    return redirect(url_for('home'))

                face = get_cropped_face(image_bytes)
                if face is None:
                    flash('Image has no face in it.', 'danger')
                    return redirect(url_for('home'))

                user_id = session['user']['id']
                image_name = file.filename
                prediction = api_identification(image_bytes, file)

            elif webcam_data:
                # Webcam Base64 Flow
                # Remove "data:image/jpeg;base64," part
                header, encoded = webcam_data.split(",", 1)
                image_bytes = base64.b64decode(encoded)

                # Create a fake FileStorage object (to pass to api_identification)
                file = FileStorage(
                    stream=io.BytesIO(image_bytes),
                    filename="webcam_capture.jpg",
                    content_type="image/jpeg"
                )

                face = get_cropped_face(image_bytes)
                if face is None:
                    flash('Webcam image has no face in it.', 'danger')
                    return redirect(url_for('home'))

                user_id = session['user']['id']
                image_name = "webcam_capture.jpg"
                prediction = api_identification(image_bytes, file)

            else:
                flash('No image provided (upload or webcam).', 'danger')
                return redirect(url_for('home'))

            # 2️⃣ Save & return results
            if not prediction:
                flash('An error occurred.', 'danger')
                return redirect(url_for('scan'))

            message, image_id = post_image(image_name, image_bytes, prediction, user_id)
            flash('Image saved successfully.', 'success')
            return redirect(url_for('results', image_id=image_id))

        except Exception as e:
            return exception_error(e, 'home')


@app.route('/results/<int:image_id>', methods=['GET'])
def results(image_id):
    try:
        image = Post.query.get_or_404(image_id)
        # Encode original uploaded image
        image_url = base_encode_image(image.image_data)
        prediction = image.prediction
        data_ = {
            'url': image_url,
            'age_lower': prediction['AgeRange']['Low'],
            'age_upper': prediction['AgeRange']['High'],
            'gender': prediction['Gender'],
            'emotion': prediction['Emotions'][0],
            'smiling': prediction['Smile'],
            'sunglasses': prediction['Sunglasses'],
            'eyeglasses': prediction['Eyeglasses'],

        }
        return render_template('predict.html', data=data_)
    except Exception as e:
        return exception_error(e, '/results/<int:image_id>')


@app.route('/history', methods=['GET'])
def history():
    resp = not_logged_in(session)
    if resp:
        return resp
    try:
        if request.method == 'GET':
            user_id = session['user']['id']
            posts = Post.query.filter_by(user_id=user_id).all()
            if len(posts) == 0:
                flash('No Uploads Yet', 'danger')
                return redirect(url_for('home'))
            data = []
            for post in posts:
                url = base_encode_image(post.image_data)
                prediction = post.prediction
                data.append({
                    'url': url,
                    'age_lower': prediction['AgeRange']['Low'],
                    'age_upper': prediction['AgeRange']['High'],
                    'gender': prediction['Gender'],
                    'emotion': prediction['Emotions'][0],
                    'smiling': prediction['Smile'],
                    'sunglasses': prediction['Sunglasses'],
                    'eyeglasses': prediction['Eyeglasses'],
                    'date': post.date.strftime("%B %d, %Y")
                })
            return render_template('history.html', history=data)
    except Exception as e:
        return exception_error(e, 'history')


@app.route('/settings', methods=['GET'])
def settings():
    resp = not_logged_in(session)
    if resp:
        return resp
    try:
        if request.method == 'GET':

            return render_template('settings.html', user={
                'name': session['user']['name'],
                'email': session['user']['email'],
                'date_joined': session['user']['date_joined']
            })
    except Exception as e:
        return exception_error(e, 'settings')


@app.route('/edit/password', methods=['POST'])
def change_password():
    resp = not_logged_in(session)
    if resp:
        return resp
    try:
        if request.method == 'POST':
            user_id = session['user']['id']
            user = User.query.filter_by(id=user_id).first()
            oldPassword, newPassword = get_passwords(request.form)
            if check_password(newPassword) is None:
                flash('Weak Password', 'danger')
                return redirect(url_for('settings'))
            if user.check_password(oldPassword) and newPassword != oldPassword:
                user.password = newPassword
                db.session.commit()
                # Updated successfully
                session['user'] = user.to_dict()
                flash('Password successfully updated', 'success')
                return redirect(url_for('settings'))
            # Password does not match
            flash('Password mismatch', 'danger')
            return redirect(url_for('settings'))
    except Exception as e:
        return exception_error(e, 'settings')


@app.route('/edit/email', methods=['GET', 'POST'])
def change_email():
    resp = not_logged_in(session)
    if resp:
        return resp
    try:
        if request.method == 'POST':
            password, newEmail = get_emails(request.form)
            user_id = session['user']['id']
            user = User.query.filter_by(id=user_id).first()
            if not user.check_password(password):
                flash('Wrong Credentials', 'danger')
                return redirect(url_for('settings'))
            if len(User.query.filter_by(email=newEmail).all()) != 0:
                flash('New Email Already Taken', 'danger')
                return redirect(url_for('settings'))
            user.email = newEmail
            db.session.commit()
            session['user'] = user.to_dict()
            # Updated successfully
            flash('Email has been successfully updated', 'success')
            return redirect(url_for('settings'))
    except Exception as e:
        return exception_error(e, 'settings')


@app.route('/profile', methods=['GET'])
def profile():
    resp = not_logged_in(session)
    if resp:
        return resp
    try:
        if request.method == 'GET':
            user = session['user']
            user_id = user['id']
            posts = Post.query.filter_by(user_id=user_id).all()
            data = {
                'name': user['name'],
                'username': user['username'],
                'email': user['email'],
                'date_joined': user['date_joined'],
                'total_detections': len(posts)
            }
            return render_template('profile.html', user=data)
    except Exception as e:
        print(e)
        return exception_error(e, 'profile')


@app.route('/about', methods=['GET'])
def about():
    resp = not_logged_in(session)
    if resp:
        return resp
    if request.method == 'GET':
        return render_template('about.html')


@app.route('/logout')
def logout():
    resp = not_logged_in(session)
    if resp:
        return resp
    session.pop('user', None)
    flash('Logout Successfully', 'success')
    return redirect(url_for('index'))
