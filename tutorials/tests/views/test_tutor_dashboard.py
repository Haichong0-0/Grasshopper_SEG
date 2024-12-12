from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from tutorials.models import User


class TutorDashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student_user = User.objects.create_user(
            username='student_user',
            email='student_user@example.com',
            password='password123',
            type_of_user='student'
        )
        self.admin_user = User.objects.create_user(
            username='admin_user',
            email='admin_user@example.com',
            password='password123',
            type_of_user='admin'
        )
        self.tutor_user = User.objects.create_user(
            username='tutor_user',
            email='tutor_user@example.com',
            password='password123',
            type_of_user='tutor'
        )

    def test_tutor_dashboard_access_tutor(self):
        self.client.login(username='tutor_user', password='password123')
        response = self.client.get(reverse('tutor_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutor/tutor_dashboard.html')

    def test_tutor_dashboard_access_non_tutor(self):
        self.client.login(username='student_user', password='password123')
        response = self.client.get(reverse('tutor_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'unauthorized_page.html')
        self.client.login(username='admin_user', password='password123')

        response = self.client.get(reverse('tutor_dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'unauthorized_page.html')

    def test_tutor_dashboard_access_unauthenticated(self):
        response = self.client.get(reverse('tutor_dashboard'))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('log_in')))
