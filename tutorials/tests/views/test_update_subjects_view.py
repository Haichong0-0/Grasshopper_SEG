from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from tutorials.models import Tutor, Subjects
from tutorials.forms import UpdateSubjectsForm

class UpdateSubjectsViewTest(TestCase):
    def setUp(self):
         self.tutor = Tutor.objects.create(
            username='testtutor',
            email='student@test.com',
            first_name='Test',
            last_name='tutor',
        )
         self.tutor.set_password('testpassword')
         self.tutor.save()
         self.subject1 = Subjects.objects.create(subject_name='Python')
         self.subject2 = Subjects.objects.create(subject_name='Django')

    def test_update_subjects_get(self):
        self.client.login(username='testtutor', password='testpassword')
        response = self.client.get(reverse('update_subjects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutor/update_subjects.html')
        self.assertIsInstance(response.context['form'], UpdateSubjectsForm)
        self.assertEqual(response.context['tutor'], self.tutor)

    def test_update_subjects_post_valid(self):
        self.client.login(username='testtutor', password='testpassword')
        response = self.client.post(reverse('update_subjects'), data={
            'subjects': ['python', 'django']
        })

        self.tutor.refresh_from_db()
        updated_subjects = self.tutor.subjects.all()
        self.assertIn(self.subject1, updated_subjects)
        self.assertIn(self.subject2, updated_subjects)
        self.assertRedirects(response, reverse('tutor_profile'))

    def test_update_subjects_post_invalid(self):
        self.client.login(username='testtutor', password='testpassword')
        response = self.client.post(reverse('update_subjects'), data={
            'subjects': ['invalid_subject_code']  
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutor/update_subjects.html')
        self.assertFalse(response.context['form'].is_valid())
        self.tutor.refresh_from_db()
        self.assertEqual(self.tutor.subjects.count(), 0)