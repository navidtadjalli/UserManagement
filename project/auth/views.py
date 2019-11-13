from flask import Blueprint, request
from marshmallow import ValidationError

from project.auth.models import User
from project.auth.schemas import UserSchema
from project.umg import status
from project.umg.authentication import Authentication
from project.umg.response import generate_response

user_views = Blueprint('auth', __name__)
user_schema = UserSchema()


@user_views.route('/register', methods=('POST',))
def register_web_service():
    req_data = request.get_json()

    try:
        data = user_schema.load(req_data)
    except ValidationError as err:
        return generate_response(400, err.messages)

    user = User.query.filter_by(username=data.get('username')).count()

    if user:
        return generate_response(409, {
            'username': [
                'Field must be unique.'
            ]
        })

    user = User(data)
    user.save()

    token = Authentication.generate_token(user.id)

    return generate_response(status.HTTP_200_OK, {'token': token})
