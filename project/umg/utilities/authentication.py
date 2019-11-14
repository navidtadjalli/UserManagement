import jwt
import os
import datetime

from project.umg.utilities.exceptions import TokenExpired, InvalidToken, TokenGenerationException


class Authentication(object):
    @staticmethod
    def generate_token(user_id, is_admin):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': {
                    'user_id': user_id,
                    'is_admin': is_admin
                }
            }
            return jwt.encode(
                payload,
                os.getenv('JWT_SECRET_KEY'),
                'HS256'
            ).decode("utf-8")
        except Exception as e:
            raise TokenGenerationException

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'))

            data = {
                'user_id': payload['sub']['user_id'],
                'is_admin': payload['sub']['is_admin']
            }

            return data
        except jwt.ExpiredSignatureError as e1:
            raise TokenExpired
        except jwt.InvalidTokenError:
            raise InvalidToken
