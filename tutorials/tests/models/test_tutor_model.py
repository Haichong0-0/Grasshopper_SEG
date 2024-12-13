from django.test import TestCase
from django.contrib.auth import get_user_model
from tutorials.models import Tutor


class TutorModelTest(TestCase):

    def setUp(self):
        self.tutor = Tutor.objects.create_user(
            username="rapidtutor",
            password="password123",
            email="rapid.tutor@example.com",
            bio="Experienced tutor in Java and Python"
        )

    def test_tutor_creation(self):
        self.assertEqual(self.tutor.username, "rapidtutor")
        self.assertEqual(self.tutor.email, "rapid.tutor@example.com")
        self.assertTrue(self.tutor.check_password("password123"))

    def test_tutor_bio(self):
        self.assertEqual(self.tutor.bio, "Experienced tutor in Java and Python")
        tutor_without_bio = Tutor.objects.create_user(
            username="speedtutor",
            password="password456",
            email="rapidtutor@example.com"
        )
        self.assertIsNone(tutor_without_bio.bio)

    def test_tutor_string_representation(self):
        self.assertEqual(str(self.tutor), f'Tutor: {self.tutor.username} ({self.tutor.id})')
