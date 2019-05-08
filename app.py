from settings import BlogSetting
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from models.model import Article as Article_Model
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config.from_object(BlogSetting)

api = Api(app)
db = SQLAlchemy(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,session_id')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    # 这里不能使用add方法，否则会出现 The 'Access-Control-Allow-Origin' header contains multiple values 的问题
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


class S_Articles(Schema):
    id = fields.Integer()
    title = fields.String()
    datetime = fields.DateTime()
    content = fields.Str()


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class Articles(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        # parser.add_argument('rate', type=int, help='Rate cannot be converted')
        parser.add_argument('title')
        args = parser.parse_args()
        if args['title'] is not None:
            articles_to_return = Article_Model.query.all()
            schema = S_Articles()
            articles_to_return = schema.dump(articles_to_return, len(articles_to_return))
        else:
            articles_to_return = {}
        return articles_to_return

    def post(self):
        parser = reqparse.RequestParser()
        # parser.add_argument('rate', type=int, help='Rate cannot be converted')
        parser.add_argument('title')
        parser.add_argument('content')
        args = parser.parse_args()
        article = Article_Model(title=args['title'], content=args['content'])
        db.session.add(article)
        db.session.flush()
        db.session.commit()
        return {'worked': args}

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()
        article_to_delete = Article_Model.query.filter_by(id=args['id']).first()
        from models.model import db
        db.session.delete(article_to_delete)
        db.session.commit()
        return 'article %s has been deleted' % args['id']


api.add_resource(Articles, '/api/v1/articles')

if __name__ == '__main__':
    app.config.from_object(BlogSetting)
    app.run()
