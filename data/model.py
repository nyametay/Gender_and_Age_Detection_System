from data import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    _password_hash = db.Column("password", db.String(128), nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    images = db.relationship('Post', backref='user', lazy=True)

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, plain_text_password):
        self._password_hash = generate_password_hash(plain_text_password)

    def check_password(self, plain_text_password):
        return check_password_hash(self._password_hash, plain_text_password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'password': self._password_hash,
            'date_joined': self.date_joined.strftime("%B %d, %Y")
            # No password returned
        }


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(255), nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=False)
    prediction = db.Column(db.JSON, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


def save_user(username, name, email, password):
    new_user = User(username=username, name=name, email=email)
    new_user.password = password
    db.session.add(new_user)
    db.session.commit()


def post_image(image_name, serialized_image, pred, user_id):
    new_post = Post(filename=image_name, image_data=serialized_image, prediction=pred, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return 'success', new_post.id
