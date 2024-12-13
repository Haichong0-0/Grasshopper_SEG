from django.test import TestCase
from django.contrib.auth import get_user_model
from tutorials.models import Subjects, Tutor


class SubjectModelTest(TestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username='testuser1', password='testpassword', email='testuser1@gmail.com'
        )
        self.user2 = get_user_model().objects.create_user(
            username='testuser2', password='testpassword', email='testuser2@gmail.com'
        )

    def test_create_subject(self):
        subject = Subjects.objects.create(
            subject_name='Python',
            timings='Mon, Wed, Fri - 10 AM to 12 PM',
            bio='A high-level programming language for general-purpose programming.'
        )

        self.assertEqual(subject.subject_name, 'Python')
        self.assertEqual(subject.timings, 'Mon, Wed, Fri - 10 AM to 12 PM')
        self.assertEqual(subject.bio, 'A high-level programming language for general-purpose programming.')

    def test_subject_name_uniqueness(self):
        subject1 = Subjects.objects.create(
            subject_name='Ruby on Rails',
            timings='Mon, Wed - 2 PM to 4 PM'
        )

        with self.assertRaises(Exception):
            subject2 = Subjects.objects.create(
                subject_name='Ruby on Rails',
                timings='Tue, Thu - 3 PM to 5 PM'
            )

    def test_default_tutor_list(self):
        subject = Subjects.objects.create(subject_name='Django')
        self.assertEqual(subject.tutor_list, [])

    def test_tutor_association(self):
        subject = Subjects.objects.create(subject_name='JavaScript')

        tutor = Tutor.objects.create_user(
            username='tutor1', password='password123', email='tutor1@example.com'
        )
        tutor.subjects.add(subject)

        self.assertIn(subject, tutor.subjects.all())
        self.assertEqual(subject.tutors.count(), 1)
        self.assertEqual(subject.tutors.first(), tutor)

    def test_tutor_list_on_subject_after_association(self):
        subject = Subjects.objects.create(subject_name='React')

        tutor1 = Tutor.objects.create_user(
            username='tutor1', password='password123', email='tutor1@example.com'
        )
        tutor2 = Tutor.objects.create_user(
            username='tutor2', password='password123', email='tutor2@example.com'
        )

        subject.tutor_list.extend([tutor1.id, tutor2.id])
        subject.save()
        subject.refresh_from_db()
        self.assertIn(tutor1.id, subject.tutor_list)
        self.assertIn(tutor2.id, subject.tutor_list)

    def test_subject_with_optional_fields(self):
        subject = Subjects.objects.create(
            subject_name='Node.js',
            timings='Tue, Thu - 1 PM to 3 PM',
            bio=None
        )

        self.assertIsNone(subject.bio)
        self.assertEqual(subject.timings, 'Tue, Thu - 1 PM to 3 PM')


