from django.test import TestCase
from django.urls import reverse
from tutorials.models import Student, Tutor, Invoice

class StudentInvoicesViewTestCase(TestCase):

    def setUp(self):
        self.tutor = Tutor.objects.create(
            username='testtutor',
            email='tutor@test.com',
            first_name='Tutor',
            last_name='User',
        )
        self.tutor.set_password('testpassword')
        self.tutor.save()

        self.student = Student.objects.create(
            username='teststudent',
            email='student@test.com',
            first_name='Test',
            last_name='Student',
            phone='0123456789',
        )
        self.student.set_password('testpassword')
        self.student.save()

        self.invoice1 = Invoice.objects.create(
            tutor=self.tutor,
            student=self.student,
            topic='Math Tutoring',
            no_of_classes=10,
            price_per_class=30.00,
            total_sum=300.00
        )

        self.invoice2 = Invoice.objects.create(
            tutor=self.tutor,
            student=self.student,
            topic='Science Tutoring',
            no_of_classes=5,
            price_per_class=50.00,
            total_sum=250.00
        )

    def test_student_invoices_view(self):
        login_success = self.client.login(username='teststudent', password='testpassword')
        self.assertTrue(login_success)

        response = self.client.get(reverse('invoices'))

        self.assertEqual(response.status_code, 200)

        invoices = Invoice.objects.filter(student=self.student).order_by('orderNo')
        self.assertQuerySetEqual(
            response.context['invoices'].order_by('orderNo'),
            invoices,
        )