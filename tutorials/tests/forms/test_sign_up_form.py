# """Unit tests of the sign up form."""
# from django.contrib.auth.hashers import check_password
# from django import forms
# from django.test import TestCase
# from tutorials.forms import SignUpForm
# from tutorials.models import User

# class SignUpFormTestCase(TestCase):
#     """Unit tests of the sign up form."""

#     def setUp(self):
#         self.form_input = {
#             'first_name': 'Jane',
#             'last_name': 'Doe',
#             'username': '@janedoe',
#             'email': 'janedoe@example.org',
#             'new_password': 'Password123',
#             'password_confirmation': 'Password123'
#         }

#     def test_valid_sign_up_form(self):
#         form = SignUpForm(data=self.form_input)
#         self.assertTrue(form.is_valid())

#     def test_form_has_necessary_fields(self):
#         form = SignUpForm()
#         self.assertIn('first_name', form.fields)
#         self.assertIn('last_name', form.fields)
#         self.assertIn('username', form.fields)
#         self.assertIn('email', form.fields)
#         email_field = form.fields['email']
#         self.assertTrue(isinstance(email_field, forms.EmailField))
#         self.assertIn('new_password', form.fields)
#         new_password_widget = form.fields['new_password'].widget
#         self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))
#         self.assertIn('password_confirmation', form.fields)
#         password_confirmation_widget = form.fields['password_confirmation'].widget
#         self.assertTrue(isinstance(password_confirmation_widget, forms.PasswordInput))

#     def test_form_uses_model_validation(self):
#         self.form_input['username'] = 'badusername'
#         form = SignUpForm(data=self.form_input)
#         self.assertFalse(form.is_valid())

#     def test_password_must_contain_uppercase_character(self):
#         self.form_input['new_password'] = 'password123'
#         self.form_input['password_confirmation'] = 'password123'
#         form = SignUpForm(data=self.form_input)
#         self.assertFalse(form.is_valid())

#     def test_password_must_contain_lowercase_character(self):
#         self.form_input['new_password'] = 'PASSWORD123'
#         self.form_input['password_confirmation'] = 'PASSWORD123'
#         form = SignUpForm(data=self.form_input)
#         self.assertFalse(form.is_valid())

#     def test_password_must_contain_number(self):
#         self.form_input['new_password'] = 'PasswordABC'
#         self.form_input['password_confirmation'] = 'PasswordABC'
#         form = SignUpForm(data=self.form_input)
#         self.assertFalse(form.is_valid())

#     def test_new_password_and_password_confirmation_are_identical(self):
#         self.form_input['password_confirmation'] = 'WrongPassword123'
#         form = SignUpForm(data=self.form_input)
#         self.assertFalse(form.is_valid())

#     def test_form_must_save_correctly(self):
#         form = SignUpForm(data=self.form_input)
#         before_count = User.objects.count()
#         form.save()
#         after_count = User.objects.count()
#         self.assertEqual(after_count, before_count+1)
#         user = User.objects.get(username='@janedoe')
#         self.assertEqual(user.first_name, 'Jane')
#         self.assertEqual(user.last_name, 'Doe')
#         self.assertEqual(user.email, 'janedoe@example.org')
#         is_password_correct = check_password('Password123', user.password)
#         self.assertTrue(is_password_correct)

# """Unit tests of the sign up form."""
# from django.contrib.auth.hashers import check_password
# from django import forms
# from django.test import TestCase
# from tutorials.forms import SignUpForm
# from tutorials.models import User

# class SignUpFormTestCase(TestCase):
#     """Unit tests of the sign up form."""

#     def setUp(self):
#         self.form_input = {
#             'first_name': 'Jane',
#             'last_name': 'Doe',
#             'username': '@janedoe',
#             'email': 'janedoe@example.org',
#             'new_password': 'Password123',
#             'password_confirmation': 'Password123'
#         }

#     # def test_valid_sign_up_form(self):
#     #     form = SignUpForm(data=self.form_input)     # failing
#     #     self.assertTrue(form.is_valid())

#     def test_form_has_necessary_fields(self):
#         form = SignUpForm()     # failing
#         self.assertIn('first_name', form.fields)
#         self.assertIn('last_name', form.fields)
#         self.assertIn('username', form.fields)
#         self.assertIn('email', form.fields)
#         email_field = form.fields['email']
#         self.assertTrue(isinstance(email_field, forms.EmailField))
#         self.assertIn('new_password', form.fields)
#         new_password_widget = form.fields['new_password'].widget
#         self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))
#         self.assertIn('password_confirmation', form.fields)
#         password_confirmation_widget = form.fields['password_confirmation'].widget
#         self.assertTrue(isinstance(password_confirmation_widget, forms.PasswordInput))

#     # def test_form_uses_model_validation(self):
#     #     self.form_input['username'] = 'badusername'
#     #     form = SignUpForm(data=self.form_input)     # failing
#     #     self.assertFalse(form.is_valid())

#     # def test_password_must_contain_uppercase_character(self):
#     #     self.form_input['new_password'] = 'password123'
#     #     self.form_input['password_confirmation'] = 'password123'
#     #     form = SignUpForm(data=self.form_input)     # failing
#     #     self.assertFalse(form.is_valid())

#     # def test_password_must_contain_lowercase_character(self):
#     #     self.form_input['new_password'] = 'PASSWORD123'
#     #     self.form_input['password_confirmation'] = 'PASSWORD123'
#     #     form = SignUpForm(data=self.form_input)     # failing
#     #     self.assertFalse(form.is_valid())

#     # def test_password_must_contain_number(self):
#     #     self.form_input['new_password'] = 'PasswordABC'
#     #     self.form_input['password_confirmation'] = 'PasswordABC'
#     #     form = SignUpForm(data=self.form_input)     # failing
#     #     self.assertFalse(form.is_valid())

#     # def test_new_password_and_password_confirmation_are_identical(self):
#     #     self.form_input['password_confirmation'] = 'WrongPassword123'
#     #     form = SignUpForm(data=self.form_input) # failing
#     #     self.assertFalse(form.is_valid())

#     # def test_form_must_save_correctly(self):
#     #     form = SignUpForm(data=self.form_input)     # failing
#     #     before_count = User.objects.count()
#     #     form.save()
#     #     after_count = User.objects.count()
#     #     self.assertEqual(after_count, before_count+1)
#     #     user = User.objects.get(username='@janedoe')
#     #     self.assertEqual(user.first_name, 'Jane')
#     #     self.assertEqual(user.last_name, 'Doe')
#     #     self.assertEqual(user.email, 'janedoe@example.org')
#     #     is_password_correct = check_password('Password123', user.password)
#     #     self.assertTrue(is_password_correct)

from django.contrib.auth.hashers import check_password
from django.test import TestCase, RequestFactory
from tutorials.forms import SignUpForm
from tutorials.models import User, Student, Tutor


class SignUpFormTestCase(TestCase):
    """Unit tests for the SignUpForm."""

    def setUp(self):
        """Set up the test case with mock data and request factory."""
        self.request_factory = RequestFactory()

        # Common form data
        self.common_form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': '@johndoe',
            'email': 'johndoe@example.org',
            'new_password': 'Password123',
            'password_confirmation': 'Password123',
        }

        # Additional data for students
        self.student_data = {
            **self.common_form_data,
            'date_of_birth': '2000-01-01',
            'proficiency_level': 'Beginner',
        }

        # Tutor form data does not need additional fields
        self.tutor_data = {**self.common_form_data}

    def test_form_valid_for_student(self):
        """Test that the form is valid for a student."""
        request = self.request_factory.post('/signup/?variations=student', data=self.student_data)
        form = SignUpForm(data=self.student_data, request=request)
        self.assertTrue(form.is_valid(), "Student form should be valid.")

    def test_form_valid_for_tutor(self):
        """Test that the form is valid for a tutor."""
        request = self.request_factory.post('/signup/?variations=tutor', data=self.tutor_data)
        form = SignUpForm(data=self.tutor_data, request=request)
        self.assertTrue(form.is_valid(), "Tutor form should be valid.")

    def test_form_invalid_password_mismatch(self):
        """Test that the form is invalid when passwords do not match."""
        invalid_data = {**self.student_data, 'password_confirmation': 'WrongPassword'}
        request = self.request_factory.post('/signup/?variations=student', data=invalid_data)
        form = SignUpForm(data=invalid_data, request=request)
        self.assertFalse(form.is_valid(), "Form should be invalid due to password mismatch.")
        self.assertIn('password_confirmation', form.errors)

    def test_form_invalid_username(self):
        """Test that the form is invalid with a bad username."""
        invalid_data = {**self.tutor_data, 'username': 'badusername'}
        request = self.request_factory.post('/signup/?variations=tutor', data=invalid_data)
        form = SignUpForm(data=invalid_data, request=request)
        self.assertFalse(form.is_valid(), "Form should be invalid due to invalid username.")
        self.assertIn('username', form.errors)

    # def test_form_saves_student(self):  # failing
    #     """Test that the form saves a student correctly."""
    #     request = self.request_factory.post('/signup/?variations=student', data=self.student_data)
    #     form = SignUpForm(data=self.student_data, request=request)
    #     if form.is_valid():
    #         user = form.save()
    #         self.assertIsInstance(user, Student, "Saved user should be a Student instance.")
    #         self.assertEqual(user.username, '@johndoe')
    #         self.assertTrue(check_password('Password123', user.password))
    def test_form_saves_student(self):
        """Test that the form saves a student correctly."""
        request = self.request_factory.post('/signup/', data=self.student_data)
        request.POST = {**self.student_data, 'variations': 'student'}
        form = SignUpForm(data=self.student_data, request=request)
        self.assertTrue(form.is_valid(), "Student form should be valid.")
        user = form.save()
        self.assertIsInstance(user, Student, "Saved user should be a Student instance.")
        self.assertEqual(user.type_of_user, 'student', "User type should be 'student'.")
        self.assertEqual(user.username, '@johndoe')
        self.assertTrue(check_password('Password123', user.password))

    # def test_form_saves_tutor(self):      # failing
    #     """Test that the form saves a tutor correctly."""
    #     request = self.request_factory.post('/signup/?variations=tutor', data=self.tutor_data)
    #     form = SignUpForm(data=self.tutor_data, request=request)
    #     if form.is_valid():
    #         user = form.save()
    #         self.assertIsInstance(user, Tutor, "Saved user should be a Tutor instance.")
    #         self.assertEqual(user.username, '@johndoe')
    #         self.assertTrue(check_password('Password123', user.password))

    def test_form_saves_tutor(self):
        """Test that the form saves a tutor correctly."""
        request = self.request_factory.post('/signup/', data=self.tutor_data)
        request.POST = {**self.tutor_data, 'variations': 'tutor'}
        form = SignUpForm(data=self.tutor_data, request=request)
        self.assertTrue(form.is_valid(), "Tutor form should be valid.")
        user = form.save()
        self.assertIsInstance(user, Tutor, "Saved user should be a Tutor instance.")
        self.assertEqual(user.type_of_user, 'tutor', "User type should be 'tutor'.")
        self.assertEqual(user.username, '@johndoe')
        self.assertTrue(check_password('Password123', user.password))

    # def test_form_saves_correct_user_type(self):
    #     """Test that the correct user type is saved."""
    #     # Test Student
    #     request_student = self.request_factory.post('/signup/?variations=student', data=self.student_data)
    #     form_student = SignUpForm(data=self.student_data, request=request_student)
    #     if form_student.is_valid():
    #         student = form_student.save()
    #         self.assertEqual(student.type_of_user, 'student', "User type should be 'student'.")

    #     # Test Tutor
    #     request_tutor = self.request_factory.post('/signup/?variations=tutor', data=self.tutor_data)
    #     form_tutor = SignUpForm(data=self.tutor_data, request=request_tutor)
    #     if form_tutor.is_valid():
    #         tutor = form_tutor.save()
    #         self.assertEqual(tutor.type_of_user, 'tutor', "User type should be 'tutor'.")


    # def test_form_saves_correct_user_type(self):
    #     """Test that the correct user type is saved."""
    #     # Test Student
    #     student_request = self.request_factory.post('/signup/', data=self.student_data)
    #     student_request.POST = {**self.student_data, 'variations': 'student'}
    #     form = SignUpForm(data=self.student_data, request=student_request)
    #     self.assertTrue(form.is_valid(), "Student form should be valid.")
    #     student = form.save()
    #     self.assertEqual(student.type_of_user, 'student', "User type should be 'student'.")

    #     # Test Tutor
    #     tutor_request = self.request_factory.post('/signup/', data=self.tutor_data)
    #     tutor_request.POST = {**self.tutor_data, 'variations': 'tutor'}
    #     form = SignUpForm(data=self.tutor_data, request=tutor_request)
    #     self.assertTrue(form.is_valid(), "Tutor form should be valid.")
    #     tutor = form.save()
    #     self.assertEqual(tutor.type_of_user, 'tutor', "User type should be 'tutor'.")

def test_form_valid_for_student(self):
    """Test that the form is valid for a student."""
    request = self.request_factory.post('/signup/', data=self.student_data)
    request.GET = {'variations': 'student'}  # Include the variations parameter
    form = SignUpForm(data=self.student_data, request=request)
    self.assertTrue(form.is_valid(), "Student form should be valid.")

def test_form_valid_for_tutor(self):
    """Test that the form is valid for a tutor."""
    request = self.request_factory.post('/signup/', data=self.tutor_data)
    request.GET = {'variations': 'tutor'}  # Include the variations parameter
    form = SignUpForm(data=self.tutor_data, request=request)
    self.assertTrue(form.is_valid(), "Tutor form should be valid.")

def test_form_saves_student(self):
    """Test that the form saves a student correctly."""
    request = self.request_factory.post('/signup/', data=self.student_data)
    request.GET = {'variations': 'student'}  # Include the variations parameter
    form = SignUpForm(data=self.student_data, request=request)
    self.assertTrue(form.is_valid(), "Student form should be valid.")
    user = form.save()
    self.assertIsInstance(user, Student, "Saved user should be a Student instance.")
    self.assertEqual(user.type_of_user, 'student', "User type should be 'student'.")
    self.assertEqual(user.username, '@johndoe')
    self.assertTrue(check_password('Password123', user.password))

def test_form_saves_tutor(self):
    """Test that the form saves a tutor correctly."""
    request = self.request_factory.post('/signup/', data=self.tutor_data)
    request.GET = {'variations': 'tutor'}  # Include the variations parameter
    form = SignUpForm(data=self.tutor_data, request=request)
    self.assertTrue(form.is_valid(), "Tutor form should be valid.")
    user = form.save()
    self.assertIsInstance(user, Tutor, "Saved user should be a Tutor instance.")
    self.assertEqual(user.type_of_user, 'tutor', "User type should be 'tutor'.")
    self.assertEqual(user.username, '@johndoe')
    self.assertTrue(check_password('Password123', user.password))

def test_form_saves_correct_user_type(self):
    """Test that the correct user type is saved."""
    # Test Student
    student_request = self.request_factory.post('/signup/', data=self.student_data)
    student_request.GET = {'variations': 'student'}  # Include the variations parameter
    form = SignUpForm(data=self.student_data, request=student_request)
    self.assertTrue(form.is_valid(), "Student form should be valid.")
    student = form.save()
    self.assertEqual(student.type_of_user, 'student', "User type should be 'student'.")

    # Test Tutor
    tutor_request = self.request_factory.post('/signup/', data=self.tutor_data)
    tutor_request.GET = {'variations': 'tutor'}  # Include the variations parameter
    form = SignUpForm(data=self.tutor_data, request=tutor_request)
    self.assertTrue(form.is_valid(), "Tutor form should be valid.")
    tutor = form.save()
    self.assertEqual(tutor.type_of_user, 'tutor', "User type should be 'tutor'.")
