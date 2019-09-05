# from flask_restful import Resource, Api, reqparse
# from models.model import User
from flask import jsonify
from flask_login import AnonymousUserMixin, user_unauthorized

from flask_httpauth import HTTPBasicAuth
from flask import g
from . import api

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(nickname_or_token, password):
    # if nickname_or_token == '':
    #     g.current_user = AnonymousUserMixin()
    #     return True
    # if password == '':
    #     g.current_user = User.verify_auth_token(nickname_or_token)
    #     g.token_used = True
    #     return g.current_user is not None
    #
    # user = User.query.filter_by(nickname=nickname_or_token).first()
    # if not user:
    #     return False
    # g.current_user = user
    # g.token_used = False
    # # return user.verify_password(password)
    return True


def get_token():
    if g.crrent_user.is_anonymous() or g.token_used:
        return user_unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(expioration=3600),
                    'expiration': 3600})


@auth.error_handler
def auth_error():
    return 'please login'


# api.add_resource(get_token, 'api/v1/token')
