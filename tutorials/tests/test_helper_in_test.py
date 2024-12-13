from django.test import TestCase
from django.urls import reverse
from tutorials.models import Admin, Tutor, Student  # Using custom models
from unittest.mock import Mock, patch
from tutorials.tests.helpers import reverse_with_next, LogInTester, MenuTesterMixin

# created with the help of chatGPT

class ReverseWithNextTests(TestCase):
    @patch('tutorials.tests.helpers.reverse', return_value='/mock-url/')
    def test_reverse_with_next_generates_correct_url(self, mock_reverse):
        url_name = 'some_view'
        next_url = '/next-page/'
        result = reverse_with_next(url_name, next_url)
        self.assertEqual(result, '/mock-url/?next=/next-page/')

class LogInTesterTests(TestCase):
    def setUp(self):
        # Use the custom user model to create users
        self.user = Student.objects.create_user(username='testuser', password='password')
        self.client = self.client_class()
        self.log_in_tester = LogInTester()
        self.log_in_tester.client = self.client

    def test_is_logged_in_returns_true_when_user_logged_in(self):
        self.client.login(username='testuser', password='password')
        self.assertTrue(self.log_in_tester._is_logged_in())

    def test_is_logged_in_returns_false_when_user_not_logged_in(self):
        self.assertFalse(self.log_in_tester._is_logged_in())


class MenuTesterMixinTests(TestCase, MenuTesterMixin):
    def setUp(self):
        self.menu_urls = [
            reverse('password'), reverse('profile'), reverse('log_out')
        ]

    def test_assert_menu_passes_when_menu_items_present(self):
        response = Mock()
        response.status_code = 200
        response.content = (b'<a href="/password/">Password</a>'
                            b'<a href="/profile/">Profile</a>'
                            b'<a href="/log_out/">Log Out</a>')
        self.assert_menu(response)

    def test_assert_menu_raises_error_when_menu_items_missing(self):
        response = Mock()
        response.status_code = 200
        response.content = b'<a href="/other/">Other</a>'
        with self.assertRaises(AssertionError):
            self.assert_menu(response)

    def test_assert_no_menu_passes_when_menu_items_absent(self):
        response = Mock()
        response.status_code = 200
        response.content = b'<a href="/other/">Other</a>'
        self.assert_no_menu(response)

    def test_assert_no_menu_raises_error_when_menu_items_present(self):
        response = Mock()
        response.status_code = 200
        response.content = (b'<a href="/password/">Password</a>'
                            b'<a href="/profile/">Profile</a>'
                            b'<a href="/log_out/">Log Out</a>')
        with self.assertRaises(AssertionError):
            self.assert_no_menu(response)