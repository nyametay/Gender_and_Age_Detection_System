from flask import Blueprint, render_template, redirect, request, url_for, session, flash
from model import get_password, update_password, update_email, save_user, post_image, get_username_count
from model import get_details, get_post_count, get_images_data, get_last_post
from modules import get_image_path_and_name, read_image, unserialize_models, image_src, serialize_image
from modules import datagenerator, prediction_string, get_cropped_image, resize_image, get_image_src
from werkzeug.utils import secure_filename
import os


main = Blueprint('main', __name__, static_folder='static', template_folder='templates')
UPLOAD_FOLDER = 'static/files'
age_model, gender_model, age_class_model = unserialize_models()

@main.route('/', methods=['GET', 'POST'])
@main.route('/signin', methods=['GET', 'POST'])
def signin():
    try:
        if request.method == 'POST':
            username = str(request.form['username'])
            password = str(request.form['password'])
            if get_username_count(username) == 1:
                con_password = get_password(username)
                if password == con_password:
                    page_name = 'main.homepage'
                    message = 'Signed in Successfully'
                    session.permanent = True
                    session['username'] = username
                    session['password'] = password
                    flash(message, 'success')
                    return redirect(url_for(page_name))
                else:
                    page_name = 'signin.html'
                    message = 'Password mismatch'
                    flash(message, 'danger')
                    return redirect(request.url)
            else:
                page_name = 'main.signup'
                message = 'Username doesn\'t exist please create an account' 
                flash(message, 'danger')
                return redirect(url_for(page_name))
        else:
            if 'username' in session:
                flash('User already signed in', 'danger')
                return redirect(url_for('main.homepage'))
            return render_template('signin.html')
    except:
        flash('No Internet Connection Try Again', 'danger')
        return render_template('signin.html')


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    try:
        if request.method == 'POST':
            username = str(request.form['username'])
            email = str(request.form['email'])
            password = str(request.form['password'])
            confirm_password = str(request.form['confirm_password'])
            if username == '' or email == '' or password == '' or confirm_password == '':
                page_name = 'signup.html'
                message = 'Input Fields or Field Empty'
                flash(message, 'danger')
                return redirect(request.url)
            elif password != confirm_password:
                page_name = 'signup.html'
                message = 'Passwords Don\'t match'
                flash(message, 'danger')
                return redirect(request.url)
            elif password == confirm_password and len(password) >= 8:
                if get_username_count(username) == 0:
                    page_name = 'main.signin'
                    message = 'Account Created Successfully'
                    save_user(username, email, password)
                    flash(message, 'success')
                    return redirect(url_for(page_name))
                else:
                    page_name = 'main.signin'
                    message = 'Username exist please sign in'
                    flash(message, 'danger')
                    return redirect(url_for(page_name))
            elif password == confirm_password and len(password) < 8:
                page_name = 'signup.html'
                message = 'Password must be 8 or more characters long' 
                flash(message, 'danger')
                return redirect(request.url) 
        else:
            if 'username' in session:
                flash('User already signed in', 'danger')
                return redirect(url_for('main.homepage'))
            return render_template('signup.html')
    except:
        return render_template('signup.html')


@main.route('/homepage', methods=['GET', 'POST'])
def homepage():
    if 'username' in session:
        if request.method == 'GET':
            username = session['username']
            return render_template('homepage.html', username=username)
    else:
        flash('Please sign in', 'danger')
        return redirect(url_for('main.signin')) 
       

@main.route('/predict', methods=['GET', 'POST'])
def predict():
    try:
        if 'username' in session:
            if request.method == 'POST': 
                image = request.files['file']
                image_extension = str(image.filename).split('.')[-1]
                image_extensions = ['jpeg', 'jpg', 'jpe', 'jp2', 'png', 'btmp', 'dib', 'webp', 'pbm', 'pgm', 'ppm', 'pxm', 'pnm']
                if image_extension.lower() not in image_extensions:
                    message = 'File Selected Was Not An Image'
                    flash(message, 'danger')
                    return redirect(url_for('main.homepage'))
                else:
                    image.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), UPLOAD_FOLDER, secure_filename(image.filename)))
                    image_name, image_path = get_image_path_and_name()
                    cropped_image = get_cropped_image(image_path)
                    if cropped_image is None:
                        message = 'Image Has No Face In It'
                        os.remove(image_path)
                        flash(message, 'danger')
                        return redirect(url_for('main.homepage'))
                    else:
                        image = read_image(image_path)
                        image = resize_image(image)
                        serialized_image = serialize_image(image)
                        X = datagenerator(cropped_image)
                        pred = prediction_string(age_model, age_class_model, gender_model, X)
                        pred = pred.split(',')
                        username = session['username']
                        try:
                            post_image(image_name, serialized_image, pred, username)
                            message = 'Uploaded Image Result'
                        except:
                            message = 'Image exist in database'
                        img_src = image_src(image_path, image_extension, 'path')
                        dic = {
                            'message': message,
                            'image': img_src,
                            'prediction': {
                                'age': pred[0],
                                'gender': pred[1],
                                'age class': pred[2]
                            },
                            'username': username
                        }
                        data = []
                        data.append(dic)
                        return render_template('predict.html', data=data)
            else:
                username = session['username']
                try:
                    uploads_num = get_post_count(username)
                except:
                    flash('No Internet connection Try Again', 'danger')
                    return redirect(url_for('main.homepage'))
                if  uploads_num != 0:
                    data = get_last_post(username)
                    data = get_image_src(data, username)
                    data = data[:-1]
                    data[0]['username'] = username
                    data[0]['message'] = 'Last Uploaded Image'
                    return render_template('predict.html', data=data)
                else:
                    flash('No Uploads Yet', 'danger')
                    return redirect(url_for('main.homepage'))
        else:
            flash('Please sign in', 'danger')
            return redirect(url_for('main.signin'))           
    except:
        page_name = 'predict.html'
        username = session['username']
        data = {
            'username': username
        }
        return render_template(page_name, data=data)
    

@main.route('/change password', methods=['GET', 'POST'])
def changepassword():
    try: 
        if 'username' in session: 
            if request.method == 'POST':
                password = str(request.form['password'])
                new_password = str(request.form['confirm_password'])
                con_password = str(session['password'])
                username = str(session['username'])
                if password != con_password:
                    message = 'Password Mismatch'
                    flash(message, 'danger')
                    return redirect(request.url)
                else:
                    update_password(new_password, username)
                    message = 'Password Was Changed Successfully'
                    flash(message, 'success')
                    return redirect(url_for('main.homepage'))
            else:
                username = session['username']
                data = {
                    'username': username
                }
                return render_template('changepassword.html', data=data)
        else:
            flash('Please sign in', 'danger')
            return redirect(url_for('main.signin')) 
    except:
        message = 'An Error Occurred'
        data = {
                    'username': username,
                    'message': message
                }
        return render_template('changepassword.html', data=data)


@main.route('/edit email', methods=['GET', 'POST'])
def editemail():
    try: 
        if 'username' in session:  
            if request.method == 'POST':
                password = request.form['password']
                email = request.form['email']
                username = session['username']
                con_password = session['password']
                if password != con_password:
                    message = 'Password Mismatch'
                    flash(message, 'danger')
                    return redirect(request.url)
                else:
                    update_email(email, username)
                    message = 'Email Was Changed Successfully'
                    flash(message, 'success')
                    return redirect(url_for('main.homepage'))
            else:
                username = session['username']
                data = {
                    'username': username
                }
                return render_template('editmail.html', data=data)
        else:
            flash('Please sign in', 'danger')
            return redirect(url_for('main.signin')) 
    except:
        message = 'An Error Occurred'
        username = session['username']
        data = {
            'message': message,
            'username': username
        }
        return render_template('editmail.html', data=data)


@main.route('/details', methods=['GET', 'POST'])
def details():
    try:
        if 'username' in session:
            username = session['username']
            data = get_details(username) 
            uploads_num = get_post_count(username)
            data['Number Of Uploads'] = uploads_num
            data['message'] = 'Successful'
            data['category'] = 'success'
            if uploads_num != 0:
                image_data = get_images_data(username)
                data_image = get_image_src(image_data, username)
                data['prediction'] = []
                data['image'] = []
                data['image_name'] = []
                data['combined'] = []
                for info in data_image[:-1]:
                    data['prediction'].append(info['prediction'])
                    data['image'].append(info['image'])
                    data['image_name'].append(info['image_name']) 
                for i in range(len(data['image_name'])):
                    data['combined'].append([data['prediction'][i], data['image_name'][i]])
                data['size'] = len(data['image'])
            return render_template('details.html', data=data)
        else:
            flash('Please sign in', 'danger')
            return redirect(url_for('main.signin')) 
    except:
        message = 'Not Internet Connection Try Again'
        username = session['username']
        dic = {
            'message': message,
            'username': username,
            'category': 'danger'
        }
        return render_template('details.html', data=dic)


@main.route('/signout', methods=['GET', 'POST'])
def signout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('main.signin'))


