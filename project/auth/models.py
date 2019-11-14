import datetime

from project.umg.authentication import Authentication
from project.umg.base_model import db, ModelActionMixin
from project.umg.exceptions import UsernameMustBeUnique
from project.umg.hashers import PasswordHasher


class User(db.Model, ModelActionMixin):
    __tablename__ = 'auth_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(128))
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(80))
    phone_number = db.Column(db.String(14))
    is_admin = db.Column(db.Boolean, default=False)
    registration_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_login_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, data):
        self.username = data.get('username')
        self.password = PasswordHasher.encode(data.get('password'))
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.phone_number = data.get('phone_number')
        self.is_admin = data.get('is_admin')

    def __repr__(self):
        return str(self.username)

    def check_password(self, password):
        return PasswordHasher.verify(self.password, password)

    def update_last_login_date(self):
        self.update({
            'last_login_date': datetime.datetime.utcnow()
        })

    def login(self):
        self.update_last_login_date()

        return Authentication.generate_token(self.id, self.is_admin)

    def check_username_exists(self):
        user_existence = User.query.filter_by(username=self.username).first()

        return user_existence is not None

    def create_user(self):
        if self.check_username_exists():
            raise UsernameMustBeUnique

        self.save()

