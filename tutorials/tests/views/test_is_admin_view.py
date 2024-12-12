from django.test import TestCase
from django.contrib.auth import get_user_model

def is_admin(user):
    return user.is_staff

class IsAdminTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.regular_user = self.User.objects.create_user(
            username='regular_user', email='regular@example.com', password='password123', is_staff=False
        )

        self.admin_user = self.User.objects.create_user(
            username='admin_user', email='admin@example.com', password='password123', is_staff=True
        )

    def test_regular_user_is_not_admin(self):
        self.assertFalse(is_admin(self.regular_user))

    def test_admin_user_is_admin(self):
        self.assertTrue(is_admin(self.admin_user))
