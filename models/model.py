from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

model = Blueprint('model', __name__)
db = SQLAlchemy()


class User(UserMixin, db.Model):
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
