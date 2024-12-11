from django.test import TestCase
from tutorials.models import Message, Student, Admin
from tutorials.forms import MessageForm

class MessageFormTest(TestCase):

    def setUp(self):
        # Create a student and admin for testing
        self.student = Student.objects.create(
            username='teststudent',
            email='student@test.com',
            first_name='Test',
            last_name='Student',
            phone='0123456789',
        )
        self.student.set_password('testpassword')
        self.student.save()
        
        self.admin = Admin.objects.create(
            username='testadmin',
            email='admin@test.com',
            first_name='Test',
            last_name='Admin',
        )
        self.admin.set_password('testpassword')
        self.admin.save()

    def test_message_form_valid_data(self):
        # Valid data for the form
        data = {
            'subject': 'Test Subject',
            'content': 'This is the content of the message.'
        }
        form = MessageForm(data=data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

        # Create the message and associate the student and admin
        message = form.save(commit=False)
        message.student = self.student
        message.admin = self.admin
        message.save()

        # Ensure that the message is saved correctly
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.first().subject, 'Test Subject')

    def test_message_form_invalid_data_missing_subject(self):
        # Invalid data (missing subject)
        data = {
            'content': 'This is the content of the message.'
        }
        form = MessageForm(data=data)

        # Assert the form is invalid
        self.assertFalse(form.is_valid())

        # Check that the 'subject' field has a required error
        self.assertIn('subject', form.errors)
        self.assertEqual(form.errors['subject'], ['This field is required.'])

    def test_message_form_invalid_data_missing_content(self):
        # Invalid data (missing content)
        data = {
            'subject': 'Test Subject'
        }
        form = MessageForm(data=data)

        # Assert the form is invalid
        self.assertFalse(form.is_valid())

        # Check that the 'content' field has a required error
        self.assertIn('content', form.errors)
        self.assertEqual(form.errors['content'], ['This field is required.'])
