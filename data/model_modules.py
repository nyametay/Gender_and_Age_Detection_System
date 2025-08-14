import numpy as np
from keras.preprocessing.image import ImageDataGenerator
import cv2
import os


def resize_image(image):
    image = cv2.resize(image, (48, 48))
    return image


def data_generator(x):
    x = x / 255
    datagen = ImageDataGenerator(
        featurewise_center=False,
        # set input mean to 0 over the dataset
        samplewise_center=False,
        # set each sample mean to 0
        featurewise_std_normalization=False,
        # divide inputs by std of the dataset
        samplewise_std_normalization=False,
        # divide each input by its std
        zca_whitening=False,
        # dimension reduction
        rotation_range=5,
        # randomly rotate images in the range 5 degrees
        zoom_range=0.1,
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


'''
def unserialize_models():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    age_model_path = os.path.join(base_dir, 'models', 'age.h5')
    gender_model_path = os.path.join(base_dir, 'models', 'age.h5')
    age_class_model_path = os.path.join(base_dir, 'models', 'age.h5')
    age_model = keras.models.load_model(age_model_path)
    gender_model = keras.models.load_model(gender_model_path)
    age_class_model = keras.models.load_model(age_class_model_path)
    return age_model, gender_model, age_class_model

'''


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

    prediction = {
        'model_1': {
            'age': int(age),
            'age_class': age_class_name,
            'gender': gender_name
        }
    }
    return prediction


def get_cropped_face(image_bytes):
    # Model paths
    deploy_path = os.path.join(
        os.path.dirname(__file__),
        'static', 'files', 'deploy.prototxt'
    )
    res100_path = os.path.join(
        os.path.dirname(__file__),
        'static', 'files', 'res10_300x300_ssd_iter_140000.caffemodel'
    )
    # Load DNN model
    net = cv2.dnn.readNetFromCaffe(deploy_path, res100_path)

    # Read image from bytes
    np_arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    (h, w) = image.shape[:2]

    # Prepare image for face detection
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    faces = []
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            startX, startY = max(0, startX), max(0, startY)
            endX, endY = min(w, endX), min(h, endY)

            cropped_face = image[startY:endY, startX:endX]
            gray_face = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2GRAY)
            resized_face = cv2.resize(gray_face, (48, 48))
            faces.append(resized_face.reshape(48, 48, 1))

    if not faces:
        return None
    elif len(faces) == 1:
        return np.array(faces[0]).reshape(1, 48, 48, 1)
    else:
        return np.array(faces)


def get_prediction(cropped_image, age_model, age_class_model, gender_model):
    X = data_generator(cropped_image)
    pred = prediction_string(age_model, age_class_model, gender_model, X)
    return pred
