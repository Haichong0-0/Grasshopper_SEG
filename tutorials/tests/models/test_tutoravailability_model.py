from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model
from tutorials.models import Tutor, TutorAvailability
from django.core.exceptions import ValidationError


class TutorAvailabilityModelTest(TestCase):

    def setUp(self):
        self.tutor = Tutor.objects.create_user(
            username="rapiduser",
            password="password123",
            email="rapid@example.com"
        )

    def test_tutor_availability_creation(self):
        availability = TutorAvailability.objects.create(
            tutor=self.tutor,
            day='monday',
            starttime='09:00:00',
            endtime='12:00:00'
        )

        self.assertEqual(availability.tutor, self.tutor)
        self.assertEqual(availability.day, 'monday')
        self.assertEqual(availability.starttime, '09:00:00')
        self.assertEqual(availability.endtime, '12:00:00')

    def test_invalid_day(self):
        with self.assertRaises(ValidationError):
            availability = TutorAvailability(
                tutor=self.tutor,
                day='invalid_day',
                starttime='09:00:00',
                endtime='12:00:00'
            )
            availability.full_clean()


    def test_valid_time_range(self):
        availability = TutorAvailability.objects.create(
            tutor=self.tutor,
            day='monday',
            starttime='09:00:00',
            endtime='17:00:00'
        )

        self.assertEqual(availability.starttime, '09:00:00')
        self.assertEqual(availability.endtime, '17:00:00')

    def test_tutor_availability_foreign_key(self):
        with self.assertRaises(IntegrityError):
            TutorAvailability.objects.create(
                tutor=None,
                day='monday',
                starttime='09:00:00',
                endtime='12:00:00'
            )

