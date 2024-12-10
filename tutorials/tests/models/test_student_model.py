from django.test import TestCase
from tutorials.models import Student

class StudentModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            username="rapidz123",
            email="rapidz@example.com",
            phone="07777777777"
        )

    def test_student_creation(self):
        self.assertEqual(self.student.username, "rapidz123")
        self.assertEqual(self.student.email, "rapidz@example.com")
        self.assertEqual(self.student.phone, "07777777777")

    def test_default_phone(self):
        new_student = Student.objects.create(
            username="newstudent",
            email="newstudent@example.com"
        )
        self.assertEqual(new_student.phone, "07777777777")
