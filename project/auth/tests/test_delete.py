from project.umg.bases.base_test import BaseTest
from project.umg.utilities import status


class TestDeleteAPI(BaseTest):
    def send_delete_request(self, id):
        headers = {
            'token': self.get_login_token('admin', '123qwe!@#')
        }

        response = self.send_request(
            'delete',
            f'users/{id}',
            headers=headers
        )
        return response

    def test_endpoint_exists(self):
        response = self.send_delete_request(1)

        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_checks_existence(self):
        response = self.send_delete_request(13)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        json_response = self.load_response(response)

        self.assertIn('User does not exist.', json_response['error'])

    def test_delete_works(self):
        response = self.send_delete_request(2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.send_delete_request(2)

        json_response = self.load_response(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertIn('User does not exist.', json_response['error'])
