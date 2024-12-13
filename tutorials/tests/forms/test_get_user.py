from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.contrib.auth.hashers import make_password
from tutorials.forms import LogInForm
from unittest.mock import patch

# created with the help of chatgpt

User = get_user_model()

class LogInFormTestCase(TestCase):
    """Unit tests for the get_user method in LogInForm."""

    def setUp(self):
        """Set up test case with mock users and request factory."""
        self.factory = RequestFactory()
        # Create mock users
        self.valid_user = User.objects.create(
            username="validuser",
            password=make_password("ValidPassword123"),
        )
        self.inactive_user = User.objects.create(
            username="inactiveuser",
            password=make_password("ValidPassword123"),
            is_active=False,
        )
        self.nonexistent_user = {
            "username": "nonexistentuser",
            "password": "NonExistentPassword123",
        }

    # # def test_get_user_valid_credentials(self):
    # #     """Test get_user with valid credentials."""
    # #     data = {"username": self.valid_user.username, "password": "ValidPassword123"}
    # #     request = self.factory.post("/login/", data=data)
    # #     form = LogInForm(data=data)
    # #     user = form.get_user(request)
    # #     self.assertIsNotNone(user, "get_user should return a valid user instance.")
    # #     self.assertEqual(user, self.valid_user, "get_user should return the correct user instance.")

    # def test_get_user_invalid_password(self):
    #     """Test get_user with an invalid password."""
    #     data = {"username": self.valid_user.username, "password": "WrongPassword"}
    #     request = self.factory.post("/login/", data=data)
    #     form = LogInForm(data=data)
    #     user = form.get_user(request)
    #     self.assertIsNone(user, "get_user should return None for invalid password.")

    # # def test_get_user_nonexistent_user(self):
    # #     """Test get_user with a nonexistent user."""
    # #     data = self.nonexistent_user
    # #     request = self.factory.post("/login/", data=data)
    # #     form = LogInForm(data=data)
    # #     user = form.get_user(request)
    # #     self.assertIsNone(user, "get_user should return None for nonexistent user.")

    # def test_get_user_inactive_user(self):
    #     """Test get_user with an inactive user."""
    #     data = {"username": self.inactive_user.username, "password": "ValidPassword123"}
    #     request = self.factory.post("/login/", data=data)
    #     form = LogInForm(data=data)
    #     user = form.get_user(request)
    #     self.assertIsNone(user, "get_user should return None for inactive user.")

    # def test_get_user_invalid_form(self):
    #     """Test get_user when the form is invalid."""
    #     data = {"username": "", "password": ""}
    #     request = self.factory.post("/login/", data=data)
    #     form = LogInForm(data=data)
    #     user = form.get_user(request)
    #     self.assertIsNone(user, "get_user should return None when the form is invalid.")

    # @patch('django.contrib.auth.authenticate')
    # def test_get_user_valid_credentials(self, mock_authenticate):
    #     """Test get_user with valid credentials."""
    #     # Mock the authenticate function to return a fake user
    #     mock_user = {"username": "validuser"}
    #     mock_authenticate.return_value = mock_user
    #     data = {"username": "validuser", "password": "ValidPassword123"}
    #     request = self.factory.post("/login/", data=data)
    #     form = LogInForm(data=data)
    #     user = form.get_user(request)
    #     self.assertEqual(user, mock_user, "get_user should return the authenticated user.")
    #     mock_authenticate.assert_called_once_with(request=request, username="validuser", password="ValidPassword123")

    # @patch('django.contrib.auth.authenticate')
    # def test_get_user_invalid_password(self, mock_authenticate):
    #     """Test get_user with invalid password."""
    #     # Mock the authenticate function to return None
    #     mock_authenticate.return_value = None
    #     data = {"username": "validuser", "password": "WrongPassword"}
    #     request = self.factory.post("/login/", data=data)
    #     form = LogInForm(data=data)
    #     user = form.get_user(request)
    #     self.assertIsNone(user, "get_user should return None for invalid password.")
    #     mock_authenticate.assert_called_once_with(request=request, username="validuser", password="WrongPassword")

    # # @patch('django.contrib.auth.authenticate')
    # # def test_get_user_nonexistent_user(self, mock_authenticate):
    # #     """Test get_user with a nonexistent username."""
    # #     # Mock the authenticate function to return None
    # #     mock_authenticate.return_value = None
    # #     data = {"username": "nonexistentuser", "password": "AnyPassword"}
    # #     request = self.factory.post("/login/", data=data)
    # #     form = LogInForm(data=data)
    # #     user = form.get_user(request)
    # #     self.assertIsNone(user, "get_user should return None for nonexistent user.")
    # #     mock_authenticate.assert_called_once_with(request=request, username="nonexistentuser", password="AnyPassword")

    # @patch('django.contrib.auth.authenticate')
    # def test_get_user_invalid_form(self, mock_authenticate):
    #     """Test get_user when the form is invalid."""
    #     # Mock the authenticate function to ensure it is not called
    #     mock_authenticate.return_value = None
    #     data = {"username": "", "password": ""}
    #     request = self.factory.post("/login/", data=data)
    #     form = LogInForm(data=data)
    #     user = form.get_user(request)
    #     self.assertIsNone(user, "get_user should return None when the form is invalid.")
    #     mock_authenticate.assert_not_called()

    # # @patch('django.contrib.auth.authenticate')
    # # def test_get_user_no_password(self, mock_authenticate):
    # #     """Test get_user when no password is provided."""
    # #     # Mock the authenticate function to ensure it is not called
    # #     mock_authenticate.return_value = None
    # #     data = {"username": "validuser", "password": ""}
    # #     request = self.factory.post("/login/", data=data)
    # #     form = LogInForm(data=data)
    # #     user = form.get_user(request)
    # #     self.assertIsNone(user, "get_user should return None when no password is provided.")
    # #     mock_authenticate.assert_not_called()

    # @patch('django.contrib.auth.authenticate')
    # def test_get_user_debug_output(self, mock_authenticate):
    #     """Test get_user outputs debug information."""
    #     # Mock the authenticate function to return a fake user
    #     mock_user = {"username": "validuser"}
    #     mock_authenticate.return_value = mock_user
    #     data = {"username": "validuser", "password": "ValidPassword123"}
    #     request = self.factory.post("/login/", data=data)
    #     form = LogInForm(data=data)
    #     with self.assertLogs(level="DEBUG") as log:
    #         user = form.get_user(request)
    #     self.assertEqual(user, mock_user, "get_user should return the authenticated user.")
    #     mock_authenticate.assert_called_once_with(request=request, username="validuser", password="ValidPassword123")

    # @patch('django.contrib.auth.authenticate')
    # def test_get_user_valid_credentials(self, mock_authenticate):
    #     """Test get_user with valid credentials."""
    #     mock_user = {"username": "validuser"}
    #     mock_authenticate.return_value = mock_user
    #     request = self.factory.post("/login/", data=self.valid_data)
    #     form = LogInForm(data=self.valid_data)
    #     self.assertTrue(form.is_valid(), "The form should be valid with correct data.")
    #     user = form.get_user(request)
    #     self.assertEqual(user, mock_user, "get_user should return the authenticated user.")
    #     mock_authenticate.assert_called_once_with(request=request, username="validuser", password="ValidPassword123")

    # @patch('django.contrib.auth.authenticate')
    # def test_get_user_invalid_password(self, mock_authenticate):
    #     """Test get_user with an invalid password."""
    #     mock_authenticate.return_value = None
    #     data = {"username": "validuser", "password": "WrongPassword"}
    #     request = self.factory.post("/login/", data=data)
    #     form = LogInForm(data=data)
    #     self.assertTrue(form.is_valid(), "The form should be valid even with a wrong password.")
    #     user = form.get_user(request)
    #     self.assertIsNone(user, "get_user should return None for invalid password.")
    #     mock_authenticate.assert_called_once_with(request=request, username="validuser", password="WrongPassword")

    # @patch('django.contrib.auth.authenticate')
    # def test_get_user_nonexistent_user(self, mock_authenticate):
    #     """Test get_user with a nonexistent username."""
    #     mock_authenticate.return_value = None
    #     data = {"username": "nonexistentuser", "password": "AnyPassword"}
    #     request = self.factory.post("/login/", data=data)
    #     form = LogInForm(data=data)
    #     self.assertTrue(form.is_valid(), "The form should be valid even for nonexistent users.")
    #     user = form.get_user(request)
    #     self.assertIsNone(user, "get_user should return None for nonexistent user.")
    #     mock_authenticate.assert_called_once_with(request=request, username="nonexistentuser", password="AnyPassword")

    # def test_get_user_invalid_form(self):
    #     """Test get_user when the form is invalid."""
    #     request = self.factory.post("/login/", data=self.invalid_data)
    #     form = LogInForm(data=self.invalid_data)
    #     self.assertFalse(form.is_valid(), "The form should be invalid for empty data.")
    #     user = form.get_user(request)
    #     self.assertIsNone(user, "get_user should return None when the form is invalid.")

    # @patch('django.contrib.auth.authenticate')
    # def test_get_user_no_password(self, mock_authenticate):
    #     """Test get_user when no password is provided."""
    #     data = {"username": "validuser", "password": ""}
    #     request = self.factory.post("/login/", data=data)
    #     form = LogInForm(data=data)
    #     self.assertFalse(form.is_valid(), "The form should be invalid when the password is missing.")
    #     user = form.get_user(request)
    #     self.assertIsNone(user, "get_user should return None when no password is provided.")
    #     mock_authenticate.assert_not_called()

    # def test_get_user_debug_output(self):
    #     """Test get_user outputs debug information."""
    #     data = self.valid_data
    #     request = self.factory.post("/login/", data=data)
    #     form = LogInForm(data=data)
    #     with self.assertLogs(level="DEBUG") as log:
    #         form.get_user(request)
    #     self.assertTrue(any("inside get_user()" in message for message in log.output), "Debug output should include 'inside get_user()'.")

    # @patch('django.contrib.auth.authenticate')
    # def test_get_user_valid_credentials(self, mock_authenticate):
    #     """Test get_user with valid credentials."""
    #     mock_user = {"username": "validuser"}
    #     mock_authenticate.return_value = mock_user
    #     form = LogInForm(data=self.valid_data)
    #     self.assertTrue(form.is_valid(), "The form should be valid with correct data.")
    #     request = self.factory.post("/login/", data=self.valid_data)
    #     user = form.get_user(request)
    #     self.assertEqual(user, mock_user, "get_user should return the authenticated user.")
    #     mock_authenticate.assert_called_once_with(request=request, username="validuser", password="ValidPassword123")

    # @patch('django.contrib.auth.authenticate')
    # def test_get_user_invalid_password(self, mock_authenticate):
    #     """Test get_user with an invalid password."""
    #     mock_authenticate.return_value = None
    #     data = {"username": "validuser", "password": "WrongPassword"}
    #     form = LogInForm(data=data)
    #     self.assertTrue(form.is_valid(), "The form should be valid even with a wrong password.")
    #     request = self.factory.post("/login/", data=data)
    #     user = form.get_user(request)
    #     self.assertIsNone(user, "get_user should return None for invalid password.")
    #     mock_authenticate.assert_called_once_with(request=request, username="validuser", password="WrongPassword")

    # @patch('django.contrib.auth.authenticate')
    # def test_get_user_nonexistent_user(self, mock_authenticate):
    #     """Test get_user with a nonexistent username."""
    #     mock_authenticate.return_value = None
    #     data = {"username": "nonexistentuser", "password": "AnyPassword"}
    #     form = LogInForm(data=data)
    #     self.assertTrue(form.is_valid(), "The form should be valid even for nonexistent users.")
    #     request = self.factory.post("/login/", data=data)
    #     user = form.get_user(request)
    #     self.assertIsNone(user, "get_user should return None for nonexistent user.")
    #     mock_authenticate.assert_called_once_with(request=request, username="nonexistentuser", password="AnyPassword")

    # def test_get_user_invalid_form(self):
    #     """Test get_user when the form is invalid."""
    #     form = LogInForm(data=self.invalid_data)
    #     self.assertFalse(form.is_valid(), "The form should be invalid for empty data.")
    #     request = self.factory.post("/login/", data=self.invalid_data)
    #     user = form.get_user(request)
    #     self.assertIsNone(user, "get_user should return None when the form is invalid.")

    # @patch('builtins.print')
    # def test_get_user_debug_output(self, mock_print):
    #     """Test get_user outputs debug information."""
    #     form = LogInForm(data=self.valid_data)
    #     self.assertTrue(form.is_valid(), "The form should be valid with correct data.")
    #     request = self.factory.post("/login/", data=self.valid_data)
    #     form.get_user(request)
    #     mock_print.assert_any_call("inside get_user().")