from functools import wraps

from flask import request

from project.umg.utilities import exceptions
from project.umg.utilities.authentication import Authentication


def is_admin(func):
    @wraps(func)
    def authorize_user(*args, **kwargs):
        token = request.headers.get('token')

        if not token:
            raise exceptions.LoginRequired

        data = Authentication.decode_token(token)

        if not data['is_admin']:
            raise exceptions.PermissionDenied

        return func(*args, **kwargs)

    return authorize_user
