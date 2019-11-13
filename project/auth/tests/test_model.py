import unittest

from project.auth.models import User


class UserModelTest(unittest.TestCase):
    def test_model_fields(self):
        columns = User.__table__.columns

        assert 'id' in columns
        assert 'username' in columns
        assert 'password' in columns
        assert 'first_name' in columns
        assert 'last_name' in columns
        assert 'phone_number' in columns
        assert 'is_admin' in columns
        assert 'registration_date' in columns
