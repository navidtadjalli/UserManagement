import unittest

from project.auth.models import User


class UserModelTest(unittest.TestCase):
    def test_model_fields(self):
        columns = User.__table__.columns

        self.assertIn('id', columns)
        self.assertIn('username', columns)
        self.assertIn('password', columns)
        self.assertIn('first_name', columns)
        self.assertIn('last_name', columns)
        self.assertIn('phone_number', columns)
        self.assertIn('is_admin', columns)
        self.assertIn('registration_date', columns)
        self.assertIn('last_login_date', columns)
