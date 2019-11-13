from project.umg.tests.base_test import BaseTest


class TestProfileUpdateAPI(BaseTest):
    def test_endpoint_exists(self):
        response = self.send_request(
            'get',
            '/profile'
        )

        assert response.status_code != 404
