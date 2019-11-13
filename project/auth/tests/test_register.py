import json
import unittest

from project.auth.models import User
from project.umg.app import create_app, db


class TestRegisterAPI(unittest.TestCase):
    def setUp(self):
        app = create_app('development')
        self.client = app.test_client()

        user = User({
            'username': 'test',
            'password': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'phone_number': '09353942996'
        })

        with app.app_context():
            db.drop_all()
            db.create_all()
            user.save()

    def test_endpoint_exist(self):
        response = self.client.post(
            '/auth/register',
            content_type='application/json'
        )
        assert response.status_code != 404

    def send_register_request(self, username, password, first_name, last_name, phone_number):
        response = self.client.post(
            '/auth/register',
            content_type='application/json',
            data=json.dumps({
                'username': username,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'phone_number': phone_number,
            })
        )

        return response

    def test_register_validates_all_parameters(self):
        response = self.send_register_request(None, None, None, None, None)

        assert response.status_code == 400

        text_response = response.get_data(as_text=True)
        json_response = json.loads(text_response)

        assert 'Field may not be null.' in json_response['username']
        assert 'Field may not be null.' in json_response['password']
        assert 'Field may not be null.' in json_response['first_name']
        assert 'Field may not be null.' in json_response['last_name']
        assert 'Field may not be null.' in json_response['phone_number']

    def test_register_validates_used_username(self):
        response = self.send_register_request('test', 'test', 'test', 'test', '09353942996')

        assert response.status_code == 409

        text_response = response.get_data(as_text=True)
        json_response = json.loads(text_response)

        assert 'Field must be unique.' in json_response['username']

    def test_register_token(self):
        response = self.send_register_request('test2', 'test2', 'test2', 'test2', '09353942996')

        assert response.status_code == 200

        text_response = response.get_data(as_text=True)
        json_response = json.loads(text_response)

        assert 'token' in json_response
        assert json_response['token'] is not None

    def test_register_validates_invalid_phone_number(self):
        response = self.send_register_request('test3', 'test3', 'test3', 'test3', '12312312312')

        assert response.status_code == 400

        text_response = response.get_data(as_text=True)
        json_response = json.loads(text_response)

        assert 'Phone number is invalid.' in json_response['phone_number']
