from django.test import TestCase
from tutorials.models import Message, Student, Admin
from tutorials.forms import MessageForm


class MessageFormTest(TestCase):

    def setUp(self):
        self.student = Student.objects.create_user(username="johndoe", password="password", email="john@example.com")
        self.admin = Admin.objects.create(username="AdminName", password="password12",
                                          email="admin@example.com")

    def test_message_form_valid_data(self):
        data = {
            'tutor_name': 'Tutor Name',
            'subject': 'Test Subject',
            'content': 'This is the content of the message.'
        }
        form = MessageForm(data=data)
        self.assertTrue(form.is_valid())
        message = form.save(commit=False)
        message.student = self.student
        message.admin = self.admin
        message.save()
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.first().subject, 'Test Subject')

    def test_message_form_invalid_data_missing_tutor_name(self):
        data = {
            'subject': 'Test Subject',
            'content': 'This is the content of the message'
        }
        form = MessageForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('tutor_name', form.errors)

    def test_message_form_invalid_data_missing_subject(self):
        data = {
            'tutor_name': 'Tutor Name',
            'content': 'This is the content of the message.'
        }
        form = MessageForm(data=data)

        self.assertFalse(form.is_valid())




