from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from tutorials.models import Message, Student  # Import the Student model


class AdminMessagesViewTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin_user = User.objects.create_user(username='admin', password='password', email='rapidadmin@gmail.com')
        self.admin_user.is_staff = True
        self.admin_user.save()
        self.student = Student.objects.create(username='student', password='password123', email='rapid2@gmail.com')
        self.message1 = Message.objects.create(content="Message 1", student=self.student)
        self.message2 = Message.objects.create(content="Message 2", student=self.student)

    def test_admin_access(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('admin_messages'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/admin_messages.html')
        messages = response.context['messages']
        self.assertEqual(messages.count(), 2)
        self.assertEqual(messages.first().content, "Message 2")

    def test_non_admin_access(self):
        self.client.login(username='student', password='password123')
        response = self.client.get(reverse('admin_messages'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('log_in')}?next={reverse('admin_messages')}")

    def test_unauthenticated_access(self):

        response = self.client.get(reverse('admin_messages'))

        self.assertRedirects(response, f"{reverse('log_in')}?next={reverse('admin_messages')}")

