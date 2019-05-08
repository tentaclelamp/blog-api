from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@localhost/BLOG"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(50))


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
