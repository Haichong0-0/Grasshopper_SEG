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

        self.lesson1 = Lesson.objects.create(
            tutor=self.tutor,
            student=self.student,
            day_of_week='monday',
            start_time='10:00',
            duration=60,
            frequency='weekly',
            term='September-Christmas',
            subject='python',
            status='confirmed'
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
            status='confirmed'
        )

        self.invoice1 = Invoice.objects.create(
            tutor=self.tutor,
            student=self.student,
            topic='python',
            no_of_classes = 5,
            price_per_class = 20,
            total_sum = 100
        ) 

        self.invoice2 = Invoice.objects.create(
            tutor=self.tutor,
            student=self.student,
            topic='django',
            no_of_classes = 3,
            price_per_class = 20,
            total_sum = 60
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
        response = self.client.get(reverse('tutor_payment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutor/tutor_payment.html')
        self.assertEqual(response.context['total_balance_due'], 160)


    def test_tutor_profile_view(self):
        response = self.client.get(reverse('tutor_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutor/tutor_profile.html')


class SortingViewsTestCase(TestCase):
    
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

        self.lesson1 = Lesson.objects.create(
            tutor=self.tutor,
            student=self.student,
            day_of_week='monday',
            start_time='10:00',
            duration=60,
            frequency='weekly',
            term='September-Christmas',
            subject='python',
            status='Confirmed'
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
            status='Confirmed'
        )

        self.invoice1 = Invoice.objects.create(
            tutor=self.tutor,
            student=self.student,
            topic='python',
            no_of_classes = 5,
            price_per_class = 20,
            total_sum = 100
        ) 

        self.invoice2 = Invoice.objects.create(
            tutor=self.tutor,
            student=self.student,
            topic='django',
            no_of_classes = 3,
            price_per_class = 20,
            total_sum = 60
        ) 
         

    def test_sort_lessons_by_subject_asc(self):
        response = self.client.get(reverse('tutor_sort_lessons'), {'sort': 'subject_asc'})
        print('Sorting by subject ascending')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutor/tutor_schedule.html')
        lessons = list(response.context['confirmed_lessons'])
        lesson_subjects = [lesson.subject for lesson in lessons]
        print(lesson_subjects)  
        self.assertEqual(lesson_subjects, ['django', 'python'])

    def test_sort_lessons_by_subject_desc(self):
        response = self.client.get(reverse('tutor_sort_lessons'), {'sort': 'subject_desc'})
        print('Sorting by subject descending')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutor/tutor_schedule.html')
        lessons = list(response.context['confirmed_lessons'])
        lesson_subjects = [lesson.subject for lesson in lessons]
        print(lesson_subjects)  
        self.assertEqual(lesson_subjects, ['python', 'django'])


        

    def test_sort_lessons_by_date_asc(self):
        response = self.client.get(reverse('tutor_sort_lessons'), {'sort': 'date_asc'})
        self.assertEqual(response.status_code, 200)
        print("sorting asc")
        self.assertTemplateUsed(response, 'tutor/tutor_schedule.html')
        lessons = list(response.context['confirmed_lessons'])
        sorted_start_times = sorted([lesson.start_time for lesson in lessons])
        lesson_start_times = [lesson.start_time for lesson in lessons]
        print(lesson_start_times)
        self.assertEqual(lesson_start_times, sorted_start_times)

    def test_sort_lessons_by_date_desc(self):
        response = self.client.get(reverse('tutor_sort_lessons'), {'sort': 'date_desc'})
        self.assertEqual(response.status_code, 200)
        print("sorting desc")
        self.assertTemplateUsed(response, 'tutor/tutor_schedule.html')
        
        lessons = list(response.context['confirmed_lessons'])
        sorted_start_times_desc = sorted([lesson.start_time for lesson in lessons], reverse=True)
        lesson_start_times_desc = [lesson.start_time for lesson in lessons]
        print(lesson_start_times_desc)
        self.assertEqual(lesson_start_times_desc, sorted_start_times_desc)



    def test_sort_invoices_by_price_asc(self):
        response = self.client.get(reverse('tutor_sort_invoices'), {'sort': 'price_asc'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutor/tutor_payment.html')
        invoices = list(response.context['invoices'])
        self.assertEqual([invoice.total_sum for invoice in invoices], [Decimal('60.00'), Decimal('100.00')])

    def test_sort_invoices_by_price_desc(self):
        response = self.client.get(reverse('tutor_sort_invoices'), {'sort': 'price_desc'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutor/tutor_payment.html')
        invoices = list(response.context['invoices'])
        self.assertEqual([invoice.total_sum for invoice in invoices], [Decimal('100.00'), Decimal('60.00')])



    