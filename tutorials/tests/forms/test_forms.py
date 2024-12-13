from django import forms
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from tutorials.forms import LogInForm, SignUpForm
from tutorials.models import User

User = get_user_model()

# created with the help of chatGPT

class LogInFormTestCase(TestCase):
    """Unit tests of the log in form."""

    fixtures = ['tutorials/tests/fixtures/default_user.json']

    def setUp(self):
        self.factory = RequestFactory()
        self.form_input = {'username': '@janedoe', 'password': 'Password123'}

    def test_form_contains_required_fields(self):
        form = LogInForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        password_field = form.fields['password']
        self.assertTrue(isinstance(password_field.widget, forms.PasswordInput))

    def test_form_accepts_valid_input(self):
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_username(self):
        self.form_input['username'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_password(self):
        self.form_input['password'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_incorrect_username(self):
        self.form_input['username'] = 'ja'
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_incorrect_password(self):
        self.form_input['password'] = 'pwd'
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_can_authenticate_valid_user(self):
        fixture = User.objects.get(username='@johndoe')
        form_input = {'username': '@johndoe', 'password': 'Password123'}
        form = LogInForm(data=form_input)
        request = self.factory.post("/login/", data=form_input)
        user = form.get_user(request)  # Pass the request object here
        self.assertEqual(user, fixture)

    def test_invalid_credentials_do_not_authenticate(self):
        form_input = {'username': '@johndoe', 'password': 'WrongPassword123'}
        form = LogInForm(data=form_input)
        request = self.factory.post("/login/", data=form_input)
        user = form.get_user(request)  # Pass the request object here
        self.assertEqual(user, None)

    def test_blank_password_does_not_authenticate(self):
        form_input = {'username': '@johndoe', 'password': ''}
        form = LogInForm(data=form_input)
        request = self.factory.post("/login/", data=form_input)
        user = form.get_user(request)  # Pass the request object here
        self.assertEqual(user, None)

    def test_blank_username_does_not_authenticate(self):
        form_input = {'username': '', 'password': 'Password123'}
        form = LogInForm(data=form_input)
        request = self.factory.post("/login/", data=form_input)
        user = form.get_user(request)  # Pass the request object here
        self.assertEqual(user, None)


class SignUpFormTestCase(TestCase):
    """Unit tests of the sign-up form."""

    def setUp(self):
        self.factory = RequestFactory()
        self.valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }

    def test_request_object_extraction_with_data(self):
        """Test that the request object is correctly extracted when passed as 'data'."""
        data_request = self.factory.post('/signup/', data={'variations': 'student'})
        form = SignUpForm(data=self.valid_data, request=data_request)  # Pass as 'request'

        self.assertEqual(form.request, data_request, "The request object should be correctly extracted and assigned.")

    def test_request_object_extraction_with_invalid_data(self):
        """Test that the request object is None if 'request' is not provided."""
        form = SignUpForm(data=self.valid_data)  # Do not pass a request

        self.assertIsNone(form.request, "The request object should be None if not provided.")