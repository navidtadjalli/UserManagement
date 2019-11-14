from project.umg.bases.base_test import BaseTest
from project.umg.utilities import status


class TestCreateAPI(BaseTest):
    def send_create_request(self, parameters={}, token=None):
        if token:
            parameters['headers'] = {
                'token': token
            }

        response = self.send_request(
            'post',
            '/users',
            **parameters
        )

        return response

    def test_create_endpoint_exists(self):
        response = self.send_create_request()

        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_authorizes_none_authentication(self):
        response = self.send_create_request()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        json_response = self.load_response(response)

        self.assertIn('Please login.', json_response['error'])

    def test_create_authorizes_nonsense_authentication(self):
        response = self.send_create_request(
            token='IAmAUser'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        json_response = self.load_response(response)

        self.assertIn('Invalid token, please try again with a new token.', json_response['error'])

    def test_create_authorizes_not_admin_user(self):
        token = self.get_login_token('navid', '123qwe!@#')

        response = self.send_create_request(
            token=token
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        json_response = self.load_response(response)

        self.assertIn('Permission denied.', json_response['error'])

    def test_create_works(self):
        token = self.get_login_token('admin', '123qwe!@#')

        response = self.send_create_request(
            token=token,
            parameters={
                'username': 'test',
                'password': '123qwe!@#',
                'first_name': 'Test',
                'last_name': 'Testian',
                'phone_number': '09353942996'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        token = self.get_login_token('test', '123qwe!@#')

        self.assertIsNotNone(token)
