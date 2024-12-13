from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import login, SESSION_KEY

class LogOutViewTest(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(username='rapiduser', password='rapidpassword')
        self.log_out_url = reverse('log_out')
        self.home_url = reverse('home')

    def test_log_out_redirect(self):
        self.client.login(username='rapiduser', password='rapidpassword')
        response = self.client.get(self.log_out_url)
        self.assertRedirects(response, self.home_url)

    def test_user_logged_out(self):
        self.client.login(username='rapiduser', password='rapidpassword')
        self.assertIn(SESSION_KEY, self.client.session)


        self.client.get(self.log_out_url)
        self.assertNotIn(SESSION_KEY, self.client.session)