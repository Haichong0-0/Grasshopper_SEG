from django.test import TestCase
from tutorials.models import Message, Student, Admin
from tutorials.forms import MessageForm


class MessageFormTest(TestCase):

    def setUp(self):
        self.student = Student.objects.create(username="student1", email="student1@example.com", password="password")
        self.admin = Admin.objects.create(username="admin1", email="admin1@example.com", password="password")

    def test_message_form_valid(self):
        data = {
            'subject': 'Test subject',
            'content': 'This is the message content.',
            'admin': self.admin,
        }
        form = MessageForm(data)
        message = form.save(commit=False)
        message.student = self.student
        message.save()
        saved_message = Message.objects.first()
        self.assertEqual(saved_message.subject, 'Test subject')
        self.assertEqual(saved_message.content, 'This is the message content.')
        self.assertEqual(saved_message.student, self.student)


    def test_message_form_invalid(self):
        data = {
            'student': self.student,
            'admin': self.admin,

        }

        form = MessageForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('subject', form.errors)
        self.assertIn('content', form.errors)

    def test_message_form_no_admin(self):
        data = {
            'subject': 'Test subject',
            'content': 'This is the message content.',
        }

        form = MessageForm(data)
        message = form.save(commit=False)
        message.student = self.student
        message.save()
        saved_message = Message.objects.first()
        self.assertIsNone(saved_message.admin)
        self.assertEqual(saved_message.subject, 'Test subject')
        self.assertEqual(saved_message.content, 'This is the message content.')

    def test_message_creation_on_valid_form(self):
        data = {
            'subject': 'Test subject',
            'content': 'This is the message content.',
            'admin': self.admin,
        }

        form = MessageForm(data)
        message = form.save(commit=False)
        message.student = self.student
        message.save()
        self.assertEqual(Message.objects.count(), 1)
        saved_message = Message.objects.first()
        self.assertEqual(saved_message.subject, 'Test subject')
        self.assertEqual(saved_message.content, 'This is the message content.')
        self.assertEqual(saved_message.student, self.student)


    def test_message_form_invalid_subject_length(self):
        data = {
            'student': self.student,
            'admin': self.admin,
            'subject': 'x' * 256,
            'content': 'This is the message content.',
        }
        form = MessageForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('subject', form.errors)





