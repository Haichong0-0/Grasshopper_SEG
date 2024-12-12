from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from tutorials.models import Lesson, Tutor, Invoice, Student
from datetime import time


class MakePaymentViewTest(TestCase):

    def setUp(self):
        self.student = Student.objects.create(
            username='student1',
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com'
        )

        self.student.set_password('password123')
        self.student.save()

        
        self.tutor = Tutor.objects.create(
            username='tutor1',
            first_name='jowgn',
            last_name='Dwoe',
            email='jwohn.1doe@example.com'
        )

        self.tutor.set_password('password123')
        self.tutor.save()


        self.lesson1 = Lesson.objects.create(
            student=self.student,
            tutor=self.tutor,
            subject='python',
            start_time=time(9, 0),
            day_of_week='monday',
            frequency='weekly',
            term='September-Christmas',
            status='Pending',
            payment_status='Unpaid',
        )

        self.lesson1.save()

        self.lesson2 = Lesson.objects.create(
            student=self.student,
            tutor=self.tutor,
            subject='django',
            start_time=time(10, 0),
            day_of_week='tuesday',
            frequency='fortnightly',
            term='January-Easter',
            status='Late',
            payment_status='Unpaid',
        )

        self.lesson2.save()


    def test_view_lessons(self):

        self.client.login(username='student1', password='password123')

        response = self.client.get(reverse('make_payment'))
        self.assertEqual(response.status_code, 200)

        self.assertIn('unpaid_pending_lessons', response.context)
        self.assertEqual(len(response.context['unpaid_pending_lessons']), 2) 

        self.assertContains(response, 'python')
        self.assertContains(response, 'django')

    def test_make_payment(self):
        self.client.login(username='student1', password='password123')
        self.assertEqual(self.lesson1.payment_status, 'Unpaid')
        response = self.client.post(reverse('make_payment'), data={
            'subject': self.lesson1.subject,
            'start_time': self.lesson1.start_time.strftime('%H:%M:%S'),  # Correct format
            'day_of_week': self.lesson1.day_of_week
        })
        self.lesson1.refresh_from_db()
        self.assertEqual(self.lesson1.payment_status, 'Paid')
        self.assertRedirects(response, reverse('student_schedule'))
    
    def test_no_unpaid_lessons(self):
        self.client.login(username='student1', password='password123')
        self.lesson1.payment_status = 'Paid'
        self.lesson1.save()
        self.lesson2.payment_status = 'Paid'
        self.lesson2.save()

        response = self.client.get(reverse('make_payment'))

        self.assertContains(response, "You have no unpaid pending lessons.")
