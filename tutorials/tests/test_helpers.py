from django.test import TestCase, RequestFactory
from django.conf import settings
from django.http import HttpResponse
from unittest.mock import Mock
from tutorials.helpers import login_prohibited

# created with the help of chatGPT

class LoginProhibitedTests(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        self.view = Mock(return_value=HttpResponse("View response"))
        settings.REDIRECT_TO_ADMIN_WHEN_LOGGED_IN = '/admin-dashboard/'
        settings.REDIRECT_TO_TUTOR_WHEN_LOGGED_IN = '/tutor-dashboard/'
        settings.REDIRECT_TO_STUDENT_WHEN_LOGGED_IN = '/student-dashboard/'

    def test_redirects_admin_user(self):
        request = self.factory.get('/')
        request.user = Mock(is_authenticated=True, type_of_user='admin')
        decorated_view = login_prohibited(self.view)
        response = decorated_view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, settings.REDIRECT_TO_ADMIN_WHEN_LOGGED_IN)

    def test_redirects_tutor_user(self):
        request = self.factory.get('/')
        request.user = Mock(is_authenticated=True, type_of_user='tutor')
        decorated_view = login_prohibited(self.view)
        response = decorated_view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, settings.REDIRECT_TO_TUTOR_WHEN_LOGGED_IN)

    def test_redirects_student_user(self):
        request = self.factory.get('/')
        request.user = Mock(is_authenticated=True, type_of_user='student')
        decorated_view = login_prohibited(self.view)
        response = decorated_view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, settings.REDIRECT_TO_STUDENT_WHEN_LOGGED_IN)

    def test_allows_unauthenticated_user(self):
        request = self.factory.get('/')
        request.user = Mock(is_authenticated=False)
        decorated_view = login_prohibited(self.view)
        response = decorated_view(request)
        self.view.assert_called_once_with(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "View response")