from flask import Flask
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SECRET_KEY'] = '1567tay'
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=10)
app.secret_key = '1567tay'
# os.environ.get('DATABASE_URL')

db = SQLAlchemy(app)

from data import routes
