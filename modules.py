import numpy as np
from keras.preprocessing.image import ImageDataGenerator
import keras
import pickle
import base64
import sys
import cv2 
import os

def get_image_path_and_name():
    for dir in os.scandir('static/files'):
        if dir.is_file:
            image_path = dir.path
            image_name = dir.name  
    return image_name, image_path


def read_image(image_path):
    image = cv2.imread(image_path)
    return image


def resize_image(image):
    image = cv2.resize(image, (48, 48))
    return image


def serialize_image(image):
    image_data = pickle.dumps(image, protocol=pickle.HIGHEST_PROTOCOL)
    return image_data


def datagenerator(x):
   x = x / 255
   datagen = ImageDataGenerator(
        featurewise_center = False,
    # set input mean to 0 over the dataset
       samplewise_center = False,
    # set each sample mean to 0 
       featurewise_std_normalization = False,
    # divide inputs by std of the dataset
       samplewise_std_normalization=False,  
    # divide each input by its std
       zca_whitening=False,
    # dimesion reduction
       rotation_range=5, 
    # randomly rotate images in the range 5 degrees
       zoom_range = 0.1,
    # Randomly zoom image 10%
       width_shift_range=0.1, 
    # randomly shift images horizontally 10%
       height_shift_range=0.1,  
    # randomly shift images vertically 10%
       horizontal_flip=False,  
    # randomly flip images
        vertical_flip=False)
   datagen.fit(x)
   return x


def unserialize_models():
    age_model = keras.models.load_model('age.h5')
    gender_model = keras.models.load_model('gender.h5')
    age_class_model = keras.models.load_model('age_class.h5')
    return age_model, gender_model, age_class_model


def prediction_string(age_model, age_class_model, gender_model, x):
    age = np.round(age_model.predict(x))[0][0]
    gender = np.argmax(gender_model.predict(x))
    age_class = np.argmax(age_class_model.predict(x))
   
    if gender == 1:
        gender_name = 'Female'
    else:
        gender_name = 'Male'

    if age_class == 2:
        age_class_name = 'Teen Age'
    elif age_class == 1:
        age_class_name = 'Old Age'
    else:
        age_class_name = 'Middle Age'
   
    prediction = str(int(age)) + ',' + str(gender_name) + ',' + str(age_class_name)
    return prediction


def get_cropped_image(image_path):
    face_cascade = cv2.CascadeClassifier('static/haarcascades/haarcascade_frontalface_default.xml')
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray_image, 1.3, 5)
    if len(face) == 1:
        for (x, y, w, h) in face:
            cropped_gray = gray_image[y : y + h, x : x + w]
            cropped_gray_image = cv2.resize(cropped_gray, (48, 48))
            gray_image_ = np.array(cropped_gray_image.tolist())
            gray_image_ = gray_image_.reshape(1,48,48,1)
            return gray_image_
    elif len(face) > 1:
        images = []
        for (x, y, w, h) in face:
            cropped_gray = gray_image[y : y + h, x : x + w]
            cropped_gray_image = cv2.resize(cropped_gray, (48, 48))
            gray_image_ = np.array(cropped_gray_image.tolist())
            gray_image_ = gray_image_.reshape(48,48,1)
            images.append(gray_image_)
        images = np.array(images)
        return images
    else:
        return None


def encode_img(img, im_type):
    """Encodes an image as a png and encodes to base 64 for display."""
    success, encoded_img = cv2.imencode('.{}'.format(im_type), img)
    if success:
        return base64.b64encode(encoded_img).decode('utf-8')
    return ''


def image_src(image_, extension, note):
    if note == 'path':
        image = cv2.imread(image_)
        os.remove(image_)
    else:
        image = image_
    encoded_img = encode_img(image, extension)
    b64_src = 'data:image/jpeg;base64,'
    img_src = b64_src + encoded_img
    return img_src


def get_image_src_from_db(image_data):
    image = pickle.loads(image_data)
    return image


def get_image_src(image_data,username):
    images = []
    for data in image_data:
        extension = data['image_name'].split('.')[-1]
        image_data_ = data['image_data']
        data_image = get_image_src_from_db(image_data_)
        img_src = image_src(data_image, extension, 'data')
        pred = data['prediction']
        pred = pred.split(',')
        images.append({
            'image_name': data['image_name'],
            'image': img_src,
            'prediction': {
                    'age': str(pred[0][1:]),
                    'gender': str(pred[1]),
                    'age class': str(pred[2][1:-2])
            }
        })
    images.append({
        'username': username
    })
    return images