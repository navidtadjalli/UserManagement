import json
import unittest

from project.auth.models import User
from project.umg import db
from project.umg.app import create_app


class BaseTest(unittest.TestCase):
    def setUp(self):
        app = create_app('development')
        self.client = app.test_client()

        user = User({
            'username': 'navid',
            'password': '123qwe!@#',
            'first_name': 'Navid',
            'last_name': 'Tadjalli',
            'phone_number': '09353942996'
        })

        with app.app_context():
            db.drop_all()
            db.create_all()
            user.save()

    def send_request(self, method_type, endpoint, **kwargs):
        client_method_func = None
        method_type = method_type.upper()

        if method_type == 'GET':
            client_method_func = self.client.get

        if method_type == 'POST':
            client_method_func = self.client.post

        if method_type == 'PUT':
            client_method_func = self.client.put

        if method_type == 'DELETE':
            client_method_func = self.client.delete

        response = client_method_func(
            endpoint,
            content_type='application/json',
            data=json.dumps(kwargs)
        )
        return response

    @staticmethod
    def load_response(response):
        text_response = response.get_data(as_text=True)
        json_response = json.loads(text_response)

        return json_response
