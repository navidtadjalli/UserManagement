from project.umg.bases.base_test import BaseTest
from project.umg.utilities import status


class TestUpdateAPI(BaseTest):
    def send_update_request(self, id, **parameters):
        headers = {
            'token': self.get_login_token('admin', '123qwe!@#')
        }

        response = self.send_request(
            'put',
            f'users/{id}',
            headers=headers,
            **parameters
        )
        return response

    def test_endpoint_exists(self):
        response = self.send_update_request(1)

        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_checks_existence(self):
        response = self.send_update_request(13)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        json_response = self.load_response(response)

        self.assertIn('User does not exist.', json_response['error'])

    def test_update_works(self):
        update_parameters = {
            'username': 'divan',
            'password': '123qwe!@#QWE',
            'first_name': 'Divan',
            'last_name': 'Navid',
            'phone_number': '09123942996'
        }

        response = self.send_update_request(
            2,
            **update_parameters
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = self.load_response(response)

        self.assertTrue(isinstance(json_response['data'], dict))
        self.assertIn('id', json_response['data'])
        self.assertIn('username', json_response['data'])
        self.assertIn(json_response['data']['username'], update_parameters['username'])
        self.assertIn('first_name', json_response['data'])
        self.assertIn(json_response['data']['first_name'], update_parameters['first_name'])
        self.assertIn('last_name', json_response['data'])
        self.assertIn(json_response['data']['last_name'], update_parameters['last_name'])
        self.assertIn('phone_number', json_response['data'])
        self.assertIn(json_response['data']['phone_number'], update_parameters['phone_number'])

        token = self.get_login_token(update_parameters['username'], update_parameters['password'])

        self.assertIsNotNone(token)
