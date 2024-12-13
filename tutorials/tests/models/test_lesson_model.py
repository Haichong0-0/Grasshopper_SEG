from django.test import TestCase
from tutorials.models import Lesson, Student, Tutor, Invoice
from datetime import time

class LessonModelTestCase(TestCase):
    def setUp(self):

        self.student = Student.objects.create(
            username="teststudent",
            email="teststudent@example.com"
        )

        self.tutor = Tutor.objects.create(
            username="testtutor",
            email="testtutor@example.com"
        )


        self.invoice = Invoice.objects.create(
            student=self.student,
            tutor=self.tutor,
            no_of_classes=10,
            price_per_class=50.00
        )

        self.lesson = Lesson.objects.create(
            student=self.student,
            tutor=self.tutor,
            day_of_week="monday",
            start_time=time(10, 0),
            duration=60,
            frequency="weekly",
            term="September-Christmas",
            subject="python",
            status="confirmed",
            invoice_no=self.invoice
        )

    def test_lesson_creation(self):
        self.assertEqual(self.lesson.student, self.student)
        self.assertEqual(self.lesson.tutor, self.tutor)
        self.assertEqual(self.lesson.day_of_week, "monday")
        self.assertEqual(self.lesson.start_time, time(10, 0))
        self.assertEqual(self.lesson.duration, 60)
        self.assertEqual(self.lesson.frequency, "weekly")
        self.assertEqual(self.lesson.term, "September-Christmas")
        self.assertEqual(self.lesson.subject, "python")
        self.assertEqual(self.lesson.status, "confirmed")
        self.assertEqual(self.lesson.invoice_no, self.invoice)

    def test_lesson_default_values(self):
        lesson_without_status = Lesson.objects.create(
            student=self.student,
            tutor=self.tutor,
            day_of_week="tuesday",
            start_time=time(14, 0),
            duration=120,
            frequency="fortnightly",
            term="January-Easter term",
            subject="django",
            invoice_no=self.invoice
        )
        self.assertEqual(lesson_without_status.status, "Pending")

    def test_related_name_for_student(self):
        lessons = self.student.lessons.all()
        self.assertIn(self.lesson, lessons)
        self.assertEqual(lessons.count(), 1)

    def test_related_name_for_tutor(self):
        lessons = self.tutor.lessons.all()
        self.assertIn(self.lesson, lessons)
        self.assertEqual(lessons.count(), 1)

    def test_lesson_without_tutor(self):
        lesson_without_tutor = Lesson.objects.create(
            student=self.student,
            day_of_week="wednesday",
            start_time=time(16, 0),
            duration=60,
            frequency="weekly",
            term="May-July",
            subject="react",
            invoice_no=self.invoice
        )
        self.assertIsNone(lesson_without_tutor.tutor)
