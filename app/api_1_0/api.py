from flask_restful import Resource, reqparse
from models.model import Article as Article_Model
from marshmallow import Schema, fields
from models.model import db
from .auth import auth
from . import api
from ..libs.errors import ApiException


class S_Articles(Schema):
    id = fields.Integer()
    title = fields.String()
    datetime = fields.DateTime()
    content = fields.Str()


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class paramsException(ApiException):
    code = 'F400'
    msg = '参数错误'
    error_code = 0


class Articles(Resource):
    @auth.login_required
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
            # raise ApiException(msg='参数错误')
            articles_to_return = {'respCode': 'F4001', 'respMessage': '参数错误'}
        return articles_to_return

    def post(self):
        self.parser = reqparse.RequestParser()
        parser = self.parser
        # parser.add_argument('rate', type=int, help='Rate cannot be converted')
        parser.add_argument('title')
        parser.add_argument('content')
        args = parser.parse_args()
        article = Article_Model(title=args['title'], content=args['content'])
        db.session.add(article)
        db.session.flush()
        db.session.commit()
        db.session.close()
        return {'worked': args}

    @auth.login_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()
        article_to_delete = Article_Model.query.filter_by(id=args['id']).first()
        # from models.model import db
        db.session.delete(article_to_delete)
        db.session.commit()
        db.session.close()
        return 'article %s has been deleted' % args['id']


api.add_resource(Articles, '/api/v1/articles')
