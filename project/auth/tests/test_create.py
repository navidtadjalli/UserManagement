from project.umg.tests.base_test import BaseTest


class TestCreateAPI(BaseTest):
    def get_login_token(self, username, password):
        response = self.send_request(
            'post',
            '/auth/login',
            username=username,
            password=password
        )
        token = self.load_response(response)['token']
        return token

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

        assert response.status_code != 404

    def test_create_authorizes_none_authentication(self):
        response = self.send_create_request()

        assert response.status_code == 401

        json_response = self.load_response(response)

        assert 'Please login.' in json_response['error']

    def test_create_authorizes_nonsense_authentication(self):
        response = self.send_create_request(
            token='IAmAUser'
        )

        assert response.status_code == 401

        json_response = self.load_response(response)

        assert 'Invalid token, please try again with a new token.' in json_response['error']

    def test_create_authorizes_not_admin_user(self):
        token = self.get_login_token('navid', '123qwe!@#')

        response = self.send_create_request(
            token=token
        )

        assert response.status_code == 403

        json_response = self.load_response(response)

        assert 'Permission denied.' in json_response['error']

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

        assert response.status_code == 201

        token = self.get_login_token('test', '123qwe!@#')

        assert token is not None
