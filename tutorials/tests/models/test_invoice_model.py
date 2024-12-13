from django.test import TestCase
from tutorials.models import Invoice, Student, Tutor

class InvoiceModelTestCase(TestCase):
    def setUp(self):

        self.student = Student.objects.create(
            username="rapidstudent",
            email="test@student.com",
            password="password123"
        )

        self.tutor = Tutor.objects.create(
            username="rapidtutor",
            email="rapid@tutor.com",
            password="password1234"
        )


        self.invoice = Invoice.objects.create(
            student=self.student,
            tutor=self.tutor,
            no_of_classes=10,
            price_per_class=50.00
        )


        self.invoice.total_sum = self.invoice.no_of_classes * self.invoice.price_per_class
        self.invoice.save()

    def test_invoice_creation(self):
        self.assertEqual(self.invoice.no_of_classes, 10)
        self.assertEqual(self.invoice.price_per_class, 50.00)
        expected_total_sum = self.invoice.no_of_classes * self.invoice.price_per_class
        self.assertEqual(self.invoice.total_sum, expected_total_sum)

    def test_invoice_with_custom_totalsum(self):

        self.invoice.total_sum = 300.00
        self.invoice.save()
        self.assertEqual(self.invoice.total_sum, 300.00)

    def test_invoice_sum_on_update(self):

        self.invoice.no_of_classes = 10
        self.invoice.price_per_class = 50.00
        self.invoice.save()

        expected_total_sum = self.invoice.no_of_classes * self.invoice.price_per_class
        self.assertEqual(self.invoice.total_sum, expected_total_sum)


