
from django.contrib.auth.hashers import check_password
from django.test import TestCase, RequestFactory
from tutorials.forms import SignUpForm
from tutorials.models import User, Student, Tutor


class SignUpFormTestCase(TestCase):
    """Unit tests for the SignUpForm."""

# created with help of chatgpt

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