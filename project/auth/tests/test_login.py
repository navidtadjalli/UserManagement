from project.auth.models import User
from project.umg.bases.base_test import BaseTest
from project.umg.utilities import status


class TestLoginAPI(BaseTest):
    def test_login_endpoint_exist(self):
        response = self.send_request(
            'post',
            '/auth/login'
        )
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def send_login_request(self, username, password):
        response = self.send_request(
            'post',
            '/auth/login',
            username=username,
            password=password,
        )

        return response

    def test_login_validates_all_parameters(self):
        response = self.send_login_request(None, None)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        json_response = self.load_response(response)

        self.assertIn('Field may not be null.', json_response['username'])
        self.assertIn('Field may not be null.', json_response['password'])

    def test_login_unregistered_user(self):
        response = self.send_login_request('test', 'test')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        json_response = self.load_response(response)

        self.assertIn('error', json_response)
        self.assertIn('User does not exist.', json_response['error'])

    def test_login_wrong_password(self):
        response = self.send_login_request('navid', 'test')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        json_response = self.load_response(response)

        self.assertIn('error', json_response)
        self.assertIn('Username or password is wrong.', json_response['error'])

    def test_login_generates_token(self):
        response = self.send_login_request('navid', '123qwe!@#')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = self.load_response(response)

        self.assertIn('token', json_response)
        self.assertIsNotNone(json_response['token'])

    def test_login_updates_last_login_date_field(self):
        user = None

        with self.app.app_context():
            user = User.query.filter_by(username='navid').first()

        last_login_date = user.last_login_date

        self.send_login_request('navid', '123qwe!@#')

        with self.app.app_context():
            user = User.query.filter_by(username='navid').first()

        new_last_login_date = user.last_login_date

        self.assertLess(last_login_date, new_last_login_date)
