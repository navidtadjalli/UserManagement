import datetime

from project.umg.base_model import db, ModelActionMixin
from project.umg.hashers import PasswordHasher


class User(db.Model, ModelActionMixin):
    __tablename__ = 'auth_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40))
    password = db.Column(db.String(128))
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(80))
    phone_number = db.Column(db.String(14))
    is_admin = db.Column(db.Boolean)
    registration_date = db.Column(db.String(40), default=datetime.datetime.utcnow())

    def __init__(self, data):
        self.username = data.get('username')
        self.password = PasswordHasher.encode(data.get('password'))
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.phone_number = data.get('phone_number')

    def __repr__(self):
        return str(self.username)

    def check_password(self, password):
        return PasswordHasher.verify(self.password, password)
