from project.auth.models import User
from project.umg.tests.base_test import BaseTest


class TestLoginAPI(BaseTest):
    def test_login_endpoint_exist(self):
        response = self.send_request(
            'post',
            '/auth/login'
        )
        assert response.status_code != 404

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

        assert response.status_code == 400

        json_response = self.load_response(response)

        assert 'Field may not be null.' in json_response['username']
        assert 'Field may not be null.' in json_response['password']

    def test_login_unregistered_user(self):
        response = self.send_login_request('test', 'test')

        assert response.status_code == 404

        json_response = self.load_response(response)

        assert 'error' in json_response
        assert 'User does not exist.' in json_response['error']

    def test_login_wrong_password(self):
        response = self.send_login_request('navid', 'test')

        assert response.status_code == 401

        json_response = self.load_response(response)

        assert 'error' in json_response
        assert 'Username or password is wrong.' in json_response['error']

    def test_login_generates_token(self):
        response = self.send_login_request('navid', '123qwe!@#')

        assert response.status_code == 200

        json_response = self.load_response(response)

        assert 'token' in json_response
        assert json_response['token'] is not None

    def test_login_updates_last_login_date_field(self):
        user = None

        with self.app.app_context():
            user = User.query.filter_by(username='navid').first()

        last_login_date = user.last_login_date

        self.send_login_request('navid', '123qwe!@#')

        with self.app.app_context():
            user = User.query.filter_by(username='navid').first()

        new_last_login_date = user.last_login_date

        assert last_login_date < new_last_login_date
