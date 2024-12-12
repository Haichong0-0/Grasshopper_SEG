from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from tutorials.models import Message, Student, Admin
from tutorials.forms import MessageForm

class LeaveMessageViewTest(TestCase):
    def setUp(self):
        # Create a test user and associated student
        self.student = Student.objects.create(
            username='teststudent',
            email='student@test.com',
            first_name='Test',
            last_name='Student',
            phone='0123456789',
        )
        self.student.set_password('testpassword')
        self.student.save()

    def test_get_request(self):
        self.client.login(username='teststudent', password='testpassword')
        response = self.client.get(reverse('leave_message'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/leave_message.html')

        
    def test_create_message_valid_data(self):
        self.client.login(username='teststudent', password='testpassword')
        message_data = {
            'subject': 'Test Message',
            'content': 'This is a test message content.'
        }
        response = self.client.post(reverse('leave_message'), data=message_data)
        self.assertRedirects(response, reverse('student_dashboard'))
        self.assertTrue(Message.objects.filter(
            student=self.student, 
            subject='Test Message'
        ).exists())

    def test_post_request_valid_data(self):
        self.client.login(username='teststudent', password='testpassword')
        url = reverse('leave_message')
        data = {
            'subject': 'Test Subject',
            'content': 'Test Content'
        }
        response = self.client.post(url, data)
        print(response)
        self.assertRedirects(response, reverse('student_dashboard'))
        self.assertEqual(Message.objects.count(), 1)

    def test_post_request_invalid_data(self):
        self.client.login(username='teststudent', password='testpassword')
        data = {
        'subject': '',
        'content': ''
        }
        response = self.client.post(reverse('leave_message'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertEqual(Message.objects.count(), 0)