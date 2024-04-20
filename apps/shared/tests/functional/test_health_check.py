from typing import Dict


from django.test import TestCase

URL = "/health/"


class HealthCheckTests(TestCase):
    def test_html_check(self):
        response = self.http_client.get(URL)
        self.assertEqual(response.status_code, 200)

    def test_json_check(self):
        response = self.http_client.get(URL, {"format": "json"})
        self.assertEqual(response.status_code, 200)

        data: Dict = response.json()
        for value in data.values():
            self.assertEqual(value, "working")
