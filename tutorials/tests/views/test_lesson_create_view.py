from django.test import TestCase
from django.urls import reverse
from tutorials.models import Lesson, Student
from tutorials.forms import LessonForm
from datetime import time

class LessonCreateViewTestCase(TestCase):

    def setUp(self):
        self.student = Student.objects.create(
            username='teststudent',
            email='student@test.com',
            first_name='Test',
            last_name='Student',
            phone='0123456789',
        )
        self.student.set_password('testpassword')
        self.student.save()

        self.client.login(username='teststudent', password='testpassword')

        self.url = reverse('lesson_create')

        self.valid_form_data = {
            'subject': 'python',
            'frequency': 'weekly',
            'term': 'May-July',
            'day_of_week': 'monday',
            'start_time': '10:00',
            'duration': 60,
        }

    def test_get_lesson_create_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/lesson_form.html')
        self.assertIsInstance(response.context['form'], LessonForm)

    def test_post_valid_lesson_create_view(self):
        self.client.login(username='teststudent', password='testpassword')
        response = self.client.post(self.url, data=self.valid_form_data)
        print(response.status_code)
        print(response.content)

        self.assertRedirects(response, reverse('student_schedule'))

        lessons = Lesson.objects.filter(student=self.student, subject='python')
        self.assertTrue(lessons.exists())
        created_lesson = lessons.first()

        self.assertEqual(created_lesson.subject, self.valid_form_data['subject'])
        self.assertEqual(created_lesson.frequency, self.valid_form_data['frequency'])
        self.assertEqual(created_lesson.term, self.valid_form_data['term'])
        self.assertEqual(created_lesson.day_of_week, self.valid_form_data['day_of_week'])
        self.assertEqual(created_lesson.duration, int(self.valid_form_data['duration']))


    def test_post_invalid_form(self):
        self.client.login(username='teststudent', password='testpassword')

        invalid_data = self.valid_form_data.copy()
        invalid_data['start_time'] = ''

        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, 200)

        if hasattr(response, 'context') and 'form' in response.context:
            form = response.context['form']
            self.assertFalse(form.is_valid())
        else:
            self.fail("The form is not in the response context, or the response did not render a template.")


    def test_post_lesson_conflict(self):
        # Create an existing lesson that will conflict with the new lesson
        existing_lesson = Lesson.objects.create(
            student=self.student,
            subject='python',
            frequency='weekly',
            term='May-July',
            day_of_week='monday',
            start_time=time(10, 0),  # Same time
            duration=60,  # Same duration
        )

        # Initial lesson count
        initial_lesson_count = Lesson.objects.filter(student=self.student).count()

        # Prepare the new lesson data (this will conflict with the existing lesson)
        conflicting_lesson_data = {
            'subject': 'python',
            'frequency': 'weekly',
            'term': 'May-July',
            'day_of_week': 'monday',  # Same day
            'start_time': '10:00',  # Same start time
            'duration': 60,  # Same duration
        }

        # Post the new conflicting lesson
        response = self.client.post(self.url, data=conflicting_lesson_data)

        # Assert that the response status is 200 (the form page with errors)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/lesson_form.html')

        # Ensure no new lesson was created because of the conflict
        self.assertEqual(Lesson.objects.filter(student=self.student).count(), initial_lesson_count)

        # Check if the form has the correct error message for the conflict
        self.assertFormError(
            response.context['form'],
            'start_time',
            'This lesson conflicts with another lesson in your schedule.',
        )



    def test_post_late_lesson_request(self):
        late_data = self.valid_form_data.copy()
        late_data['term'] = 'September-Christmas'  # Modify term to a late request term

        # Step 1: Send the POST request without the 'submit_anyway' parameter
        response = self.client.post(self.url, data=late_data)
        
        # Step 2: Check the response and ensure the term warning is shown
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/lesson_form.html')
        self.assertIn('LATE REQUEST', response.context['term_warning'])
        self.assertEqual(response.context['submit'], 'Submit Anyway')

        # Step 3: Add the 'submit_anyway' field and submit the form
        late_data['submit_anyway'] = 'Submit Anyway'  # Ensure the field matches the button text
        response = self.client.post(self.url, data=late_data)

        # Step 4: Check if the response redirects to the student schedule
        self.assertEqual(response.status_code, 302)  # Redirect after successful submission

        # Step 5: Ensure the lesson status is set to 'Late'
        self.assertTrue(
            Lesson.objects.filter(student=self.student, subject='python', status='Late').exists()
        )


