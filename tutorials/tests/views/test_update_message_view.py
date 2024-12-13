from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from tutorials.models import Message, Student, Admin   

class UpdateMessageStatusViewTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin_user = Admin.objects.create_user(username='admin', password='password', email='admin@example.com')
        self.admin_user.is_staff = True
        self.admin_user.save()


        self.student = Student.objects.create(username='student',password='password1234',email='student2@gmail.com')

        self.message = Message.objects.create(content="Message 1", student=self.student, status='pending')

    def test_admin_access_post(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(
            reverse('update_message_status', args=[self.message.id]),
            data={'status': 'resolved'}
        )

        self.message.refresh_from_db()

        self.assertEqual(self.message.status, 'resolved')

        self.assertRedirects(response, reverse('admin_messages'))

    def test_invalid_status_post(self):
        self.client.login(username='admin', password='password')

        response = self.client.post(
            reverse('update_message_status', args=[self.message.id]),
            data={'status': 'invalid_status'}
        )

        self.message.refresh_from_db()

        self.assertEqual(self.message.status, 'pending')

        self.assertRedirects(response, reverse('admin_messages'))

    def test_non_admin_access(self):
        self.client.login(username='student', password='password123')


        response = self.client.post(
            reverse('update_message_status', args=[self.message.id]),
            data={'status': 'resolved'}
        )

        self.assertEqual(response.status_code, 302)

        self.message.refresh_from_db()

        self.assertEqual(self.message.status, 'pending')

    def test_nonexistent_message(self):
        self.client.login(username='admin', password='password')

        response = self.client.post(
            reverse('update_message_status', args=[9999]),
            data={'status': 'resolved'}
        )

        self.assertEqual(response.status_code, 404)

    def test_unauthenticated_access(self):
        response = self.client.post(
            reverse('update_message_status', args=[self.message.id]),
            data={'status': 'resolved'}
        )

        self.assertRedirects(response, f"{reverse('log_in')}?next={reverse('update_message_status', args=[self.message.id])}")