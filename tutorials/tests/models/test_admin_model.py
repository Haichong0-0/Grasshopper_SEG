from django.test import TestCase
from tutorials.models import Admin

class AdminModelTest(TestCase):

    def setUp(self):
        self.admin = Admin.objects.create_user(
            username="adminuser",
            password="password123",
            email="admin@example.com",
            first_name="Admin",
            last_name="User"
        )

    def test_admin_creation(self):
        self.assertEqual(self.admin.username, "adminuser")
        self.assertEqual(self.admin.email, "admin@example.com")
        self.assertTrue(self.admin.check_password("password123"))

    def test_admin_string_representation(self):
        self.assertEqual(str(self.admin), "Admin: Admin User")

    def test_admin_full_name(self):

        self.assertEqual(self.admin.get_full_name(), "Admin User")
