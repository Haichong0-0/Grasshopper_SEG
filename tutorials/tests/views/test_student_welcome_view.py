from django.test import TestCase
from django.urls import reverse
from tutorials.models import Student

class StudentWelcomeViewTestCase(TestCase):

    def setUp(self):
        self.student = Student.objects.create(
            username='teststudent',
            email='student@test.com',
            first_name='Test',
            last_name='Student',
            phone='0123456789',
        )
        self.student.set_password('testpassword')
        self.student.save()

    def test_student_welcome_view_authenticated(self):
        login_success = self.client.login(username='teststudent', password='testpassword')
        self.assertTrue(login_success)

        response = self.client.get(reverse('student_welcome'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'student/student_welcome.html')

    def test_student_welcome_view_not_authenticated(self):
        response = self.client.get(reverse('student_welcome'))
        self.assertEqual(response.status_code, 302)