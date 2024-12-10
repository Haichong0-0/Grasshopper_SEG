from django.test import TestCase
from tutorials.models import Message, Student, Admin

class MessageModelTestCase(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            username="teststudent",
            email="teststudent@example.com"
        )
        self.admin = Admin.objects.create(
            username="testadmin",
            email="testadmin@example.com"
        )
        self.message = Message.objects.create(
            student=self.student,
            admin=self.admin,
            subject="Test Subject",
            content="This is a test message.",
            status="pending"
        )

    def test_message_creation(self):
        self.assertEqual(self.message.student, self.student)
        self.assertEqual(self.message.admin, self.admin)
        self.assertEqual(self.message.subject, "Test Subject")
        self.assertEqual(self.message.content, "This is a test message.")
        self.assertEqual(self.message.status, "pending")
        self.assertIsNotNone(self.message.created_at)

    def test_message_status_change(self):
        self.message.status = "resolved"
        self.message.save()
        self.assertEqual(self.message.status, "resolved")

    def test_message_without_admin(self):
        message_without_admin = Message.objects.create(
            student=self.student,
            subject="Subject without Admin",
            content="This message has no assigned admin."
        )
        self.assertIsNone(message_without_admin.admin)
        self.assertEqual(message_without_admin.status, "pending")

    def test_related_name(self):
        messages = self.student.messages.all()
        self.assertIn(self.message, messages)
        self.assertEqual(messages.count(), 1)
