from project.auth.models import User
from project.umg.bases.base_test import BaseTest
from project.umg.utilities import status


class TestRegisterAPI(BaseTest):
    def test_endpoint_exist(self):
        response = self.send_request(
            'post',
            '/auth/register'
        )
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def send_register_request(self, username, password, first_name, last_name, phone_number):
        response = self.send_request(
            'post',
            '/auth/register',
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )

        return response

    def test_register_validates_all_parameters(self):
        response = self.send_register_request(None, None, None, None, None)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        json_response = self.load_response(response)

        self.assertIn('Field may not be null.', json_response['username'])
        self.assertIn('Field may not be null.', json_response['password'])
        self.assertIn('Field may not be null.', json_response['first_name'])
        self.assertIn('Field may not be null.', json_response['last_name'])
        self.assertIn('Field may not be null.', json_response['phone_number'])

    def test_register_validates_used_username(self):
        response = self.send_register_request('navid', 'test', 'test', 'test', '09353942996')

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        json_response = self.load_response(response)

        self.assertIn('Field must be unique.', json_response['username'])

    def test_register_generates_token(self):
        response = self.send_register_request('test2', 'test2', 'test2', 'test2', '09353942996')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = self.load_response(response)

        self.assertIn('token', json_response)
        self.assertIsNotNone(json_response['token'])

    def test_register_validates_invalid_phone_number(self):
        response = self.send_register_request('test3', 'test3', 'test3', 'test3', '12312312312')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        json_response = self.load_response(response)

        self.assertIn('Phone number is invalid.', json_response['phone_number'])

    def test_register_saves_user_as_normal_user(self):
        response = self.send_register_request('test3', 'test3', 'test3', 'test3', '09353942996')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with self.app.app_context():
            user = User.query.filter_by(username='test3').first()

        self.assertFalse(user.is_admin)
        self.assertEqual('test3', str(user))
