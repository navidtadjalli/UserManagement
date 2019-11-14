from flask import Flask

from project.umg import bcrypt, db, status
from project.umg.base_exception import APIException
from marshmallow import ValidationError
from project.umg.config import app_config

from project.auth.views import auth_views, user_views

from project.auth.models import User
from project.umg.response import generate_response


def create_app(env_name):
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])

    bcrypt.init_app(app)

    db.init_app(app)

    app.register_blueprint(auth_views, url_prefix='/auth')
    app.register_blueprint(user_views, url_prefix='/users')

    @app.errorhandler(APIException)
    def handle_invalid_usage(error):
        return generate_response(error.status_code, error.to_dict())

    @app.errorhandler(ValidationError)
    def handle_invalid_usage(error):
        return generate_response(status.HTTP_400_BAD_REQUEST, error.messages)

    return app
