from flask import Blueprint
from flask_restful import Api

errors = {
    'UserAlreadyExistsError': {
        'message': "A user with that username already exists.",
        'status': 409,
    },
    'ResourceDoesNotExist': {
        'message': "A resource with that ID no longer exists.",
        'status': 410,
        'extra': "Any extra information you want.",
    },
}

api_bp = Blueprint('api', __name__)
api = Api(api_bp, catch_all_404s=True, errors=errors)

from .api import db
