from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

class StudentDashboardViewTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_student_dashboard_view_authenticated(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/student_dashboard_in.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], 'Student!')

