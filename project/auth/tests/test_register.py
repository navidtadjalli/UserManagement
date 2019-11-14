from project.auth.models import User
from project.umg.tests.base_test import BaseTest


class TestRegisterAPI(BaseTest):
    def test_endpoint_exist(self):
        response = self.send_request(
            'post',
            '/auth/register'
        )
        assert response.status_code != 404

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

        assert response.status_code == 400

        json_response = self.load_response(response)

        assert 'Field may not be null.' in json_response['username']
        assert 'Field may not be null.' in json_response['password']
        assert 'Field may not be null.' in json_response['first_name']
        assert 'Field may not be null.' in json_response['last_name']
        assert 'Field may not be null.' in json_response['phone_number']

    def test_register_validates_used_username(self):
        response = self.send_register_request('navid', 'test', 'test', 'test', '09353942996')

        assert response.status_code == 409

        json_response = self.load_response(response)

        assert 'Field must be unique.' in json_response['username']

    def test_register_generates_token(self):
        response = self.send_register_request('test2', 'test2', 'test2', 'test2', '09353942996')

        assert response.status_code == 200

        json_response = self.load_response(response)

        assert 'token' in json_response
        assert json_response['token'] is not None

    def test_register_validates_invalid_phone_number(self):
        response = self.send_register_request('test3', 'test3', 'test3', 'test3', '12312312312')

        assert response.status_code == 400

        json_response = self.load_response(response)

        assert 'Phone number is invalid.' in json_response['phone_number']

    def test_register_saves_user_as_normal_user(self):
        response = self.send_register_request('test3', 'test3', 'test3', 'test3', '09353942996')

        assert response.status_code == 200

        with self.app.app_context():
            user = User.query.filter_by(username='navid').first()

        assert user.is_admin == False
