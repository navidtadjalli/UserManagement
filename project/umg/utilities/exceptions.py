from project.umg.utilities import status
from project.umg.bases.base_exception import APIException


class UsernameMustBeUnique(APIException):
    status_code = status.HTTP_409_CONFLICT
    field = 'username'
    message = 'Field must be unique.'


class UserDoesNotExist(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'User does not exist.'


class UsernameOrPasswordIsWrong(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = 'Username or password is wrong.'


class LoginRequired(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = 'Please login.'


class TokenExpired(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = 'Token expired, please login again.'


class InvalidToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = 'Invalid token, please try again with a new token.'


class TokenGenerationException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Error in generating user token.'


class PermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    message = 'Permission denied.'
