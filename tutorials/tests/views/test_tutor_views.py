from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model 
from tutorials.models import Tutor, Student, Lesson, Invoice
from decimal import Decimal



class TutorViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.tutor = Tutor.objects.create_user(username='tutor', email='tutor@email.com', password='password', type_of_user='tutor')
        self.client.login(username='tutor', password='password')

        self.student = Student.objects.create_user(
            username='student', 
            email='student@email.com',
            password='password', 
            type_of_user='student'
        )
        self.student.set_password('password')
        self.student.save()


        self.invoice1 = Invoice.objects.create(
            tutor=self.tutor,
            student=self.student,
            topic='python',
            no_of_classes = 5,
            price_per_class = 20,
            total_sum = 100
        ) 
        self.invoice1.save()

        self.invoice2 = Invoice.objects.create(
            tutor=self.tutor,
            student=self.student,
            topic='django',
            no_of_classes = 3,
            price_per_class = 20,
            total_sum = 60
        ) 
        self.invoice2.save()


        self.lesson1 = Lesson.objects.create(
            tutor=self.tutor,
            student=self.student,
            day_of_week='monday',
            start_time='10:00',
            duration=60,
            frequency='weekly',
            term='September-Christmas',
            subject='python',
            status='Confirmed',
            invoice_no= self.invoice1
        )
        self.lesson2 = Lesson.objects.create(
            tutor=self.tutor,
            student=self.student,
            day_of_week='tuesday',
            start_time='11:00',
            duration=120,
            frequency='fortnightly',
            term='January-Easter term',
            subject='django',
            status='Confirmed',
            invoice_no= self.invoice2
        )
         

    def test_tutor_schedule_view(self):
       
        self.client.login(username='tutor', password='password')
        response = self.client.get(reverse('tutor_schedule'))
        self.assertEqual(response.status_code, 200)
        print(response.status_code)
        self.assertTemplateUsed(response, 'tutor/tutor_schedule.html')
        self.assertIn('confirmed_lessons', response.context)
        self.assertEqual(len(response.context['confirmed_lessons']), 2)
        
  

    def test_tutor_payments_view(self):
        self.client.login(username='tutor', password='password')
        response = self.client.get(reverse('tutor_payment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutor/tutor_payment.html')
        self.assertEqual(response.context['total_balance'], 160)


    def test_tutor_profile_view(self):
        self.client.login(username='tutor', password='password')
        response = self.client.get(reverse('tutor_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutor/tutor_profile.html')







    