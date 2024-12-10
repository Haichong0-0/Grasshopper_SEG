from django.test import TestCase
from tutorials.models import Invoice


class InvoiceModelTestCase(TestCase):
    def setUp(self):

        self.invoice = Invoice.objects.create(
            no_of_classes=5,
            price_per_class=50.00
        )

    def test_invoice_creation(self):
        self.assertEqual(self.invoice.no_of_classes, 5)
        self.assertEqual(self.invoice.price_per_class, 50.00)
        self.assertEqual(self.invoice.totalsum, 0)

    def test_calc_sum(self):
        self.invoice.calc_sum()
        self.assertEqual(self.invoice.totalsum, 250.00)

    def test_invoice_with_custom_totalsum(self):
        self.invoice.totalsum = 300.00
        self.assertEqual(self.invoice.totalsum, 300.00)

    def test_invoice_sum_on_update(self):
        self.invoice.no_of_classes = 10
        self.invoice.price_per_class = 50.00
        self.invoice.calc_sum()
        self.assertEqual(self.invoice.totalsum, 500.00)
