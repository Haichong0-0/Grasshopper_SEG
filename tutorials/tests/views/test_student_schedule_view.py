from django.test import TestCase
from django.urls import reverse
from tutorials.models import Lesson, Student
from datetime import time

class StudentScheduleViewTestCase(TestCase):

    def setUp(self):
        # Create a student user
        self.student = Student.objects.create(
            username='test',
            email='test@hotmail.com',
            first_name='testing',
            last_name='test',
            phone='07777777777',
        )
        self.student.set_password('test123')  # Ensure password is hashed
        self.student.save()

        # Create lessons with different statuses
        self.lesson_confirmed = Lesson.objects.create(
            student=self.student,
            start_time=time(10, 0),
            duration=60,
            status='Confirmed',
            term='September-Christmas',
            day_of_week='monday',
            subject='python',
            frequency='weekly'
        )

        self.lesson_pending = Lesson.objects.create(
            student=self.student,
            start_time=time(11, 0),
            duration=60,
            status='Pending',
            term='September-Christmas',
            day_of_week='monday',
            subject='java',
            frequency='weekly'
        )

        self.lesson_late = Lesson.objects.create(
            student=self.student,
            start_time=time(12, 0),
            duration=60,
            status='Late',
            term='September-Christmas',
            day_of_week='monday',
            subject='c++',
            frequency='weekly'
        )

        self.lesson_rejected = Lesson.objects.create(
            student=self.student,
            start_time=time(13, 0),
            duration=60,
            status='Rejected',
            term='September-Christmas',
            day_of_week='monday',
            subject='javascript',
            frequency='weekly'
        )

    def test_student_schedule_view(self):
        # Log in the student user
        login_success = self.client.login(username='test', password='test123')
        self.assertTrue(login_success)  # Ensure login is successful

        # Access the schedule page
        response = self.client.get(reverse('student_schedule'))

        # Check that the response status is OK (200)
        self.assertEqual(response.status_code, 200)


        # Check that the correct lessons are passed to the template
        # For confirmed lessons
        confirmed_lessons = Lesson.objects.filter(student=self.student, status='Confirmed').order_by('start_time')
        self.assertQuerySetEqual(
            response.context['confirmed_lessons'],
            confirmed_lessons,
        )

        # For pending and late lessons
        pending_lessons = Lesson.objects.filter(student=self.student, status__in=['Pending', 'Late']).order_by('start_time')
        self.assertQuerySetEqual(
            response.context['pending_lessons'],
            pending_lessons,
        )

        # For rejected lessons
        rejected_lessons = Lesson.objects.filter(student=self.student, status='Rejected').order_by('start_time')
        self.assertQuerySetEqual(
            response.context['rejected_lessons'],
            rejected_lessons,
        )

    def test_student_without_lessons(self):
        # Create a user with no lessons
        self.student = Student.objects.create(
            username='test2',
            email='test2@hotmail.com',
            first_name='testing',
            last_name='test',
            phone='07778777777',
        )
        self.student.set_password('test123')
        self.student.save()

        # Log in the new user
        self.client.login(username='test2', password='test123')

        # Access the schedule page
        response = self.client.get(reverse('student_schedule'))

        # Check that no lessons are passed to the template
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['confirmed_lessons']), 0)
        self.assertEqual(len(response.context['pending_lessons']), 0)
        self.assertEqual(len(response.context['rejected_lessons']), 0)
