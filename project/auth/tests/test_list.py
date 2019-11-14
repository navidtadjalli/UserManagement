from project.umg.bases.base_test import BaseTest
from project.umg.utilities import status


class TestListAPI(BaseTest):
    def send_list_request(self, token=None):
        headers = {}

        if token:
            headers['token'] = token

        response = self.send_request(
            'get',
            'users',
            headers=headers
        )
        return response

    def test_endpoint_exists(self):
        response = self.send_list_request()

        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list_works(self):
        token = self.get_login_token('admin', '123qwe!@#')

        response = self.send_list_request(token=token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = self.load_response(response)

        self.assertIn('data', json_response)
        self.assertTrue(isinstance(json_response['data'], list))
        self.assertIn('id', json_response['data'][0])
        self.assertIn('username', json_response['data'][0])
        self.assertIn('first_name', json_response['data'][0])
        self.assertIn('last_name', json_response['data'][0])
        self.assertIn('phone_number', json_response['data'][0])
        self.assertIn('registration_date', json_response['data'][0])
        self.assertIn('last_login_date', json_response['data'][0])
