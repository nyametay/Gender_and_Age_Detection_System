from flask import redirect, flash, url_for
import requests
import base64
import re


def not_logged_in(session):
    if 'user' not in session:
        flash('Not Logged In Yet', 'danger')
        return redirect(url_for('login'))
    return None


def is_logged_in(session):
    if 'user' in session:
        flash('Already Logged In', 'danger')
        return redirect(url_for('home'))
    return None


def get_signin_details(body):
    username = str(body['username'])
    password = str(body['password'])
    return username, password


def get_signup_details(body):
    username = str(body['username'])
    name = str(body['name'])
    email = str(body['email'])
    password = str(body['password'])
    return name, username, email, password


def exception_error(e, path):
    print(str(e))
    flash('An error occurred', 'danger')
    return redirect(url_for(path))


def check_password(password):
    has_alpha = re.search(r'[a-zA-Z]', password) is not None
    has_num = re.search(r'[0-9]', password) is not None
    has_symbol = re.search(r'[^a-zA-Z0-9]', password) is not None

    if has_alpha and has_num and has_symbol and len(password) >= 8:
        return 'valid'
    return None


def get_passwords(body):
    oldPassword = str(body['current_password']).strip()
    newPassword = str(body['new_password']).strip()
    return oldPassword, newPassword


def get_emails(body):
    oldPassword = str(body['password']).strip()
    newEmail = str(body['new_email']).lower().strip()
    return oldPassword, newEmail


def base_encode_image(image):
    image_base64 = base64.b64encode(image).decode("utf-8")
    image_url = f"data:image/jpeg;base64,{image_base64}"
    return image_url


def api_identification(image, file):
    url = "https://faceanalyzer-ai.p.rapidapi.com/faceanalysis"

    files = {
        "image": (file.filename, image, file.content_type)  # (filename, file_object, MIME type)
    }

    headers = {
        "x-rapidapi-key": "5627c10ccfmsh38f6e0451025facp1438d0jsn8cf0a26c96be",
        "x-rapidapi-host": "faceanalyzer-ai.p.rapidapi.com"
    }

    response = requests.post(url, files=files, headers=headers)

    print(response.status_code)
    print(type(response.status_code))
    if response.status_code != 200:
        return None
    response = response.json()
    body = response.get('body')
    faces = body.get('faces')
    if len(faces) == 1:
        face = faces[0]
        facial_features = face.get('facialFeatures')
        return facial_features
    elif len(faces) == 0:
        return None
    data = []
    for face in faces:
        facial_features = face.get('facialFeatures')
        data.append(facial_features)
    return data
