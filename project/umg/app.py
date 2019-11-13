from flask import Flask

from project.umg import bcrypt, db
from project.umg.config import app_config

from project.auth.views import user_views

from project.auth.models import User


def create_app(env_name):
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])

    bcrypt.init_app(app)

    db.init_app(app)

    app.register_blueprint(user_views, url_prefix='/auth')

    @app.route('/', methods=['GET'])
    def index():
        return 'Congratulations! Your first endpoint is workin'

    return app
