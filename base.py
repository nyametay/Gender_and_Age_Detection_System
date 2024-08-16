from flask import Flask
from routes import main
from datetime import timedelta


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '1567tay'
    app.config['UPLOAD_FOLDER'] = 'static/files'
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://intaylor:9X6letKDo4gJPwxIDGECmHoRhFht7sgG@dpg-ci488ldiuie031gv8mf0-a.oregon-postgres.render.com/project_f0bg'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.permanent_session_lifetime = timedelta(days=10)
    app.secret_key = '1567tay'
    #os.environ.get('DATABASE_URL')

    app.register_blueprint(main)

    return app





