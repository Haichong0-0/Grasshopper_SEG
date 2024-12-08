from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError  # Import the correct exception
from django.test import TestCase
from django.contrib.auth import get_user_model
from tutorials.models import Subjects

class SubjectsModelTest(TestCase):

    def setUp(self):
        # Create a user instance
        self.user = get_user_model().objects.create_user(
            username="rapiduser",
            password="password123",
            email="rapid@example.com"
        )

    def test_subject_creation(self):
        # Create a subject instance with a valid user
        subject = Subjects.objects.create(
            user=self.user,
            subject='python',
            proficiency=Subjects.INTERMEDIATE
        )
        self.assertEqual(subject.user, self.user)
        self.assertEqual(subject.subject, 'python')
        self.assertEqual(subject.proficiency, Subjects.INTERMEDIATE)

    def test_subject_default_proficiency(self):
        subject = Subjects.objects.create(
            user=self.user,
            subject='ruby_on_rails'
        )

        self.assertEqual(subject.proficiency, Subjects.INTERMEDIATE)

    def test_invalid_subject(self):
        with self.assertRaises(ValidationError):
            subject = Subjects(
                user=self.user,
                subject='Invalid_Subject',
                proficiency=Subjects.BEGINNER
            )
            subject.full_clean()

    def test_invalid_proficiency(self):
        with self.assertRaises(ValidationError):
            subject = Subjects(
                user=self.user,
                subject='Python',
                proficiency='invalid_proficiency'
            )
            subject.full_clean()
    def test_subject_foreign_key(self):
        with self.assertRaises(IntegrityError):
            Subjects.objects.create(
                subject='Javascript',
                proficiency=Subjects.MASTERY
            )
