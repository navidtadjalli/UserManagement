from project.umg.bases.base_test import BaseTest
from project.umg.utilities import status


class TestUpdateAPI(BaseTest):
    def send_get_request(self, id):
        headers = {
            'token': self.get_login_token('admin', '123qwe!@#')
        }

        response = self.send_request(
            'get',
            f'users/{id}',
            headers=headers
        )
        return response

    def test_endpoint_exists(self):
        response = self.send_get_request(1)

        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_checks_existence(self):
        response = self.send_get_request(13)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        json_response = self.load_response(response)

        self.assertIn('User does not exist.', json_response['error'])

    def test_get_works(self):
        response = self.send_get_request(2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = self.load_response(response)

        self.assertTrue(isinstance(json_response['data'], dict))
        self.assertIn('id', json_response['data'])
        self.assertIn('username', json_response['data'])
        self.assertIn('first_name', json_response['data'])
        self.assertIn('last_name', json_response['data'])
        self.assertIn('phone_number', json_response['data'])
