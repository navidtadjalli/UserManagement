from flask import Blueprint, request
from marshmallow import ValidationError

from project.auth.models import User
from project.auth import schemas
from project.umg import status
from project.umg.authentication import Authentication
from project.umg.response import generate_response

user_views = Blueprint('auth', __name__)
user_schema = schemas.UserSchema()
user_login_schema = schemas.UserLoginSchema()


@user_views.route('/register', methods=('POST',))
def register_web_service():
    req_data = request.get_json()

    try:
        data = user_schema.load(req_data)
    except ValidationError as err:
        return generate_response(status.HTTP_400_BAD_REQUEST, err.messages)

    user_existence = User.query.filter_by(username=data.get('username')).count()

    if user_existence:
        return generate_response(status.HTTP_409_CONFLICT, {
            'username': [
                'Field must be unique.'
            ]
        })

    user = User(data)
    user.save()

    token = Authentication.generate_token(user.id)

    return generate_response(status.HTTP_200_OK, {'token': token})


@user_views.route('/login', methods=('POST',))
def login():
    req_data = request.get_json()

    try:
        data = user_login_schema.load(req_data)
    except ValidationError as err:
        return generate_response(status.HTTP_400_BAD_REQUEST, err.messages)

    user = User.query.filter_by(username=data.get('username')).first()

    if not user:
        return generate_response(status.HTTP_404_NOT_FOUND, {
            'error': 'User does not exist.'
        })

    if not user.check_password(data.get('password')):
        return generate_response(status.HTTP_401_UNAUTHORIZED, {
            'error': 'Username or password is wrong.'
        })

    token = Authentication.generate_token(user.id)

    return generate_response(status.HTTP_200_OK, {'token': token})
