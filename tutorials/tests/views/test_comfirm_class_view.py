from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from tutorials.models import Lesson, Tutor, Student, Admin
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

class ConfirmClassViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = Admin.objects.create(username='admintest', password='adminpass', email='admintest@example.com', type_of_user='admin')
        self.student = Student.objects.create(username='studentest', password='studentpass', email='studenttest@example.com', type_of_user='student')
        self.tutor = Tutor.objects.create(username='tutortest', password='tutorpass', email='tutortest@example.com', type_of_user='tutor')

        self.lesson = Lesson.objects.create(
            lesson_id=1,
            student=self.student,
            subject='Math',
            duration=60,
            start_time=datetime.now().time(),
            day_of_week='Monday',
            term='May-July'
        )
        self.url = reverse('confirm_class', args=[self.lesson.lesson_id])
        self.client.force_authenticate(user=self.admin_user)

    def test_confirm_class_success(self):
        response = self.client.post(self.url, {'tutor': self.tutor})
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.status, 'Pending')
        self.assertEqual(self.lesson.tutor, self.tutor)

    def test_confirm_class_invalid_data(self):
        response = self.client.post(self.url, {'tutor': ''})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_confirm_class_without_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url, {'tutor': self.tutor})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)