from flask import Blueprint, request

from project.auth.models import User
from project.auth import schemas
from project.umg import status
from project.umg.authentication import Authentication
from project.umg import exceptions
from project.umg.response import generate_response

auth_views = Blueprint('auth', __name__)
user_views = Blueprint('users', __name__)
user_schema = schemas.UserSchema()
user_login_schema = schemas.UserLoginSchema()


def create_user_object(user_data):
    data = user_schema.load(user_data)
    user = User(data)
    user.create_user()

    return user


@auth_views.route('/register', methods=('POST',))
def register_web_service():
    user = create_user_object(request.get_json())

    token = user.login()

    return generate_response(status.HTTP_200_OK, {'token': token})


@auth_views.route('/login', methods=('POST',))
def login():
    req_data = request.get_json()
    data = user_login_schema.load(req_data)

    user = User.query.filter_by(username=data.get('username')).first()

    if not user:
        raise exceptions.UserDoesNotExist

    if not user.check_password(data.get('password')):
        raise exceptions.UsernameOrPasswordIsWrong

    token = user.login()

    return generate_response(status.HTTP_200_OK, {'token': token})


@user_views.route('', methods=['POST'])
def create():
    token = request.headers.get('token')

    if not token:
        raise exceptions.LoginRequired

    data = Authentication.decode_token(token)

    if not data['is_admin']:
        raise exceptions.PermissionDenied

    create_user_object(request.get_json())

    return generate_response(status.HTTP_201_CREATED, {
        'success': True
    })
