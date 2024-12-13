from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class HomeViewTest(TestCase):
    def setUp(self):
        self.home_url = reverse('home')
        self.redirect_url = reverse('student_dashboard')
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(username='rapiduser', password='rapidpassword')

    # def test_home_page_unauthenticated(self):
    #     response = self.client.get(self.home_url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'home.html')

    # def test_redirect_if_authenticated(self):
    #     self.client.login(username='rapiduser', password='rapidpassword')
    #     response = self.client.get(self.home_url)
    #     self.assertRedirects(response, self.redirect_url)

