from django.test import TestCase
from ..factory import UserFactory


class TestDjangoAdmin(TestCase):
    def test_admin_home(self):
        # Create a superuser and force log in
        user = UserFactory(is_staff=True, is_superuser=True)
        self.force_login(user)

        # Test the page renders successfully
        response = self.http_client.get("/admin/")
        self.assertEqual(response.status_code, 200)
