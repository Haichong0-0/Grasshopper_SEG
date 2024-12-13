# 1 failure 2 errors
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from tutorials.models import Lesson, Tutor, Student, Invoice, TutorAvailability
from django.contrib.auth import get_user_model
from datetime import datetime, time, timedelta

User = get_user_model()

# created with chatgpt

class ConfirmRejectClassViewTests(TestCase):

    def setUp(self):
        """Set up test data."""
        self.admin_user = User.objects.create_user(username='admin', email='admin@example.com', password='adminpass', type_of_user='admin')
        self.student = Student.objects.create_user(username='student', email='student@example.com', password='studentpass', type_of_user='student')
        self.tutor = Tutor.objects.create_user(username='tutor', email='tutor@example.com', password='tutorpass', type_of_user='tutor')

        self.lesson = Lesson.objects.create(
            student=self.student,
            day_of_week='monday',
            start_time=time(10, 0),
            duration=60,
            frequency='weekly',
            term='September-Christmas',
            subject='python',
            status='Pending'
        )

        self.client = APIClient()

    def test_confirm_class_view(self):
        """Test the confirm class view."""
        self.client.force_authenticate(user=self.admin_user)

        url = reverse('confirm_class', kwargs={'lesson_id': self.lesson.lesson_id})
        response = self.client.post(url, {
            'tutor': self.tutor.id
        })

        self.lesson.refresh_from_db()

        # Assert the lesson was confirmed
        self.assertEqual(response.status_code, 302)  # Redirects to admin_schedule
        self.assertEqual(self.lesson.status, 'Confirmed')
        self.assertEqual(self.lesson.tutor, self.tutor)

        # Assert an invoice was created
        self.assertIsNotNone(self.lesson.invoice_no)
        invoice = self.lesson.invoice_no
        self.assertEqual(invoice.tutor, self.tutor)
        self.assertEqual(invoice.student, self.student)
        self.assertEqual(invoice.topic, self.lesson.subject)
        self.assertEqual(invoice.no_of_classes, 1)
        self.assertEqual(invoice.total_sum, 20)

        # Assert tutor availability was created
        availability = TutorAvailability.objects.get(tutor=self.tutor)
        self.assertEqual(availability.day, 'monday')
        self.assertEqual(availability.starttime, self.lesson.start_time)

    def test_reject_class_view(self):
        """Test the reject class view."""
        self.client.force_authenticate(user=self.admin_user)

        url = reverse('reject_class', kwargs={'lesson_id': self.lesson.lesson_id})
        response = self.client.post(url)

        self.lesson.refresh_from_db()

        # Assert the lesson was rejected
        self.assertEqual(response.status_code, 302)  # Redirects to admin_schedule
        self.assertEqual(self.lesson.status, 'Rejected')

    def test_invalid_tutor_in_confirm_class(self):
        """Test confirm class with invalid tutor."""
        self.client.force_authenticate(user=self.admin_user)

        url = reverse('confirm_class', kwargs={'lesson_id': self.lesson.lesson_id})
        response = self.client.post(url, {
            'tutor': 999  # Non-existent tutor ID
        })

        self.lesson.refresh_from_db()

        # Assert the lesson was not confirmed
        self.assertEqual(response.status_code, 302)  # Redirects due to failure
        self.assertEqual(self.lesson.status, 'Pending')

    def test_confirm_class_without_tutor(self):
        """Test confirm class without providing a tutor."""
        self.client.force_authenticate(user=self.admin_user)

        url = reverse('confirm_class', kwargs={'lesson_id': self.lesson.lesson_id})
        response = self.client.post(url, {})

        self.lesson.refresh_from_db()

        # Assert the lesson was not confirmed
        self.assertEqual(response.status_code, 302)  # Redirects due to failure
        self.assertEqual(self.lesson.status, 'Pending')

    def test_unauthenticated_access(self):
        """Test unauthenticated access to confirm and reject views."""
        confirm_url = reverse('confirm_class', kwargs={'lesson_id': self.lesson.lesson_id})
        reject_url = reverse('reject_class', kwargs={'lesson_id': self.lesson.lesson_id})

        confirm_response = self.client.post(confirm_url, {'tutor': self.tutor.id})
        reject_response = self.client.post(reject_url)

        # Assert access is redirected (unauthenticated users are redirected to login)
        self.assertEqual(confirm_response.status_code, 302)  # Redirect
        self.assertEqual(reject_response.status_code, 302)

    def test_non_admin_access(self):
        """Test non-admin user access to confirm and reject views."""
        self.client.force_authenticate(user=self.student)

        confirm_url = reverse('confirm_class', kwargs={'lesson_id': self.lesson.lesson_id})
        reject_url = reverse('reject_class', kwargs={'lesson_id': self.lesson.lesson_id})

        confirm_response = self.client.post(confirm_url, {'tutor': self.tutor.id})
        reject_response = self.client.post(reject_url)

        # Assert access is redirected (non-admin users are redirected or forbidden)
        self.assertEqual(confirm_response.status_code, 302)  # Redirect
        self.assertEqual(reject_response.status_code, 302)