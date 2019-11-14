from flask import Blueprint, request

from project.auth.models import User
from project.auth import schemas
from project.umg.utilities import exceptions, status
from project.umg.utilities.decorators import is_admin
from project.umg.utilities.response import generate_response

auth_views = Blueprint('auth', __name__)
user_views = Blueprint('users', __name__)
user_schema = schemas.UserSchema()
users_schema = schemas.UserSchema(many=True)
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
@is_admin
def user_create():
    create_user_object(request.get_json())

    return generate_response(status.HTTP_201_CREATED, {
        'success': True
    })


@user_views.route('', methods=['GET'])
@is_admin
def user_list():
    users = User.query.all()

    data = users_schema.dump(users)

    return generate_response(status.HTTP_200_OK, {
        'data': data
    })
