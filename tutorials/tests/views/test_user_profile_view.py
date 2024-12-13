from django.test import TestCase
from django.urls import reverse
from tutorials.models import Tutor, TutorAvailability, Subjects
from django.contrib.auth import get_user_model


class UserProfileViewTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.subject_python = Subjects.objects.create(subject_name='Python')
        self.subject_django = Subjects.objects.create(subject_name='Django')
        self.user = User.objects.create_user(username='rapiduser', password='password', email='rapidexample@gmail.com')
        self.tutor_user = Tutor.objects.create_user(username='tutoruser', password='password', email='rapid2example@gmail.com')
        self.tutor_user.bio = 'Experienced Python and Django tutor'
        self.tutor_user.save()
        self.tutor_user.subjects.add(self.subject_python, self.subject_django)
        self.availability_slot_1 = TutorAvailability.objects.create(tutor=self.tutor_user, day='Monday', starttime='9:00', endtime='10:00')
        self.availability_slot_2 = TutorAvailability.objects.create(tutor=self.tutor_user, day='Wednesday',
                                                                    starttime='10:00', endtime='11:00')

    def test_user_profile_view_for_normal_user(self):
        response = self.client.get(reverse('user_profile', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], self.user)
        self.assertIsNone(response.context['tutor'])
        self.assertEqual(len(response.context['availability_slots']), 0)