from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class AdminWelcomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.regular_user = self.User.objects.create_user(
            username='regular_user', email='regular@example.com', password='password123', is_staff=False
        )

        self.admin_user = self.User.objects.create_user(
            username='admin_user', email='admin@example.com', password='password123', is_staff=True
        )

    def test_admin_access(self):
        self.client.login(username='admin_user', password='password123')

        response = self.client.get(reverse('admin_welcome'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/admin_welcome.html')

    def test_non_admin_access(self):

        self.client.login(username='regular_user', password='password123')

        response = self.client.get(reverse('admin_welcome'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('log_in')))

    def test_unauthenticated_access(self):
        response = self.client.get(reverse('admin_welcome'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('log_in')))