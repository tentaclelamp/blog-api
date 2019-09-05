from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

model = Blueprint('model', __name__)
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.query.get(int(user_id))

    def generate_auth_token(self, expioration=3600):
        s = Serializer(current_app.confg['SECRET_KEY'], expires_in=expioration)
        return s.dump({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.load(token)
        except:
            return None
        return User.query.get(data['id'])


class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.now())
    title = db.Column(db.String(50))
    content = db.Column(db.TEXT)


class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    url = db.Column(db.String(50))
    content = db.Column(db.TEXT)
    pic = db.Column(db.String(50))
