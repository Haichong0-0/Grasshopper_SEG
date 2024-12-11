from django.test import TestCase
from django.urls import reverse
from tutorials.models import Message, Student
from tutorials.forms import MessageForm

class LeaveMessageViewTest(TestCase):

    def setUp(self):
        # Create a student for testing
        self.student = Student.objects.create(
            username='teststudent',
            email='student@test.com',
            first_name='Test',
            last_name='Student',
            phone='0123456789',
        )
        self.student.set_password('testpassword')
        self.student.save()

        # Login the student
        self.client.login(username='teststudent', password='testpassword')

        # URL for the leave message view
        self.url = reverse('leave_message')

