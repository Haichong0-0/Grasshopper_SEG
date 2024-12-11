from django.test import TestCase
from django.contrib.auth import get_user_model
from tutorials.models import Lesson, Student, Tutor
from tutorials.forms import LessonForm

class LessonFormTest(TestCase):

    def setUp(self):
        # Create a user for the tutor
        User = get_user_model()
        self.tutor = Tutor.objects.create(
            username="test_tutor",
            first_name="Test",
            last_name="Tutor",
            email="test_tutor@example.com",
            password="securepassword"
        )

        # Create a student
        self.student = Student.objects.create(
            first_name="Test",
            last_name="Student",
            email="test_student@example.com"
        )

    def test_lesson_form_valid(self):
        """
        Test that the LessonForm is valid when all required fields are provided with correct data.
        """
        form_data = {
            'subject': 'python',
            'frequency': 'weekly',
            'term': 'September-Christmas',
            'start_time': '10:00',
            'day_of_week': 'monday',
            'duration': 60,
        }
        form = LessonForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_lesson_form_invalid_missing_required_field(self):
        """
        Test that the LessonForm is invalid when a required field is missing.
        """
        form_data = {
            'frequency': 'weekly',
            'term': 'September-Christmas',
            'start_time': '10:00',
            'day_of_week': 'monday',
            'duration': 60,
        }
        form = LessonForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('subject', form.errors)

    def test_lesson_form_invalid_invalid_choice(self):
        """
        Test that the LessonForm is invalid when a field has a value not in its choices.
        """
        form_data = {
            'subject': 'invalid_subject',
            'frequency': 'weekly',
            'term': 'September-Christmas',
            'start_time': '10:00',
            'day_of_week': 'monday',
            'duration': 60,
        }
        form = LessonForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('subject', form.errors)

    def test_lesson_form_save(self):
        """
        Test that the LessonForm saves the data correctly to the database.
        """
        form_data = {
            'subject': 'python',
            'frequency': 'weekly',
            'term': 'September-Christmas',
            'start_time': '10:00',
            'day_of_week': 'monday',
            'duration': 60,
        }
        form = LessonForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Save the form and create a Lesson instance
        lesson = form.save(commit=False)
        lesson.student = self.student
        lesson.tutor = self.tutor
        lesson.save()

        # Verify the Lesson instance
        self.assertEqual(Lesson.objects.count(), 1)
        saved_lesson = Lesson.objects.first()
        self.assertEqual(saved_lesson.subject, 'python')
        self.assertEqual(saved_lesson.frequency, 'weekly')
        self.assertEqual(saved_lesson.term, 'September-Christmas')
        self.assertEqual(str(saved_lesson.start_time), '10:00:00')
        self.assertEqual(saved_lesson.day_of_week, 'monday')
        self.assertEqual(saved_lesson.duration, 60)
        self.assertEqual(saved_lesson.student, self.student)
        self.assertEqual(saved_lesson.tutor, self.tutor)
