from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from tutorials.models import Student  

class StudentProfileViewTest(TestCase):

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
         self.url = reverse('student_profile')

    def test_student_profile_view_for_authenticated_student(self):
        self.client.login(username='teststudent', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/student_profile.html')