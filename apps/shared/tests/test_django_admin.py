from django.test import TestCase, Client
from rest_framework.test import APIClient

from apps.authentication.models import User
from apps.shared.tests.factory.user import UserFactory


class TestDjangoAdmin(TestCase):
    def setUp(self):
        # API Client should be used for testing API endpoints
        self.c = APIClient()
        # http client should be used for testing regular webpages
        self.http_client = Client()

    def force_login(self, user: User):
        """
        Force log in the HTTP clients as the provided user.
        """
        self.c.force_authenticate(user)
        self.http_client.force_login(user)

    def test_admin_home(self):
        # Create a superuser and force log in
        user = UserFactory(is_staff=True, is_superuser=True)
        self.force_login(user)

        # Test the page renders successfully
        response = self.http_client.get("/admin/")
        self.assertEqual(response.status_code, 200)
