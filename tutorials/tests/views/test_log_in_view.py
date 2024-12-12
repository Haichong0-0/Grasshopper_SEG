from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponseRedirect


class LogInViewTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_get_login_page(self):
        url = reverse('log_in')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_post_login_valid_credentials(self):
        url = reverse('log_in')
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/student_dashboard/')

    def test_post_login_invalid_credentials(self):
        url = reverse('log_in')
        response = self.client.post(url, {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The credentials provided were invalid!')

    def test_redirect_when_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('log_in')
        response = self.client.get(url)
        self.assertRedirects(response, '/student_dashboard/')


