from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import render
from tutorials.decorators import user_type_required
from tutorials.models import Admin, Tutor, Student

User = get_user_model()  # Import the User model

# created with the help of chatGPT

class UserTypeRequiredDecoratorTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Create test users with unique emails
        self.admin_user = Admin.objects.create_user(
            username="admin_user",
            password="password123",
            email="admin_user@example.com",
            type_of_user="admin",
        )

        self.tutor_user = Tutor.objects.create_user(
            username="tutor_user",
            password="password123",
            email="tutor_user@example.com",
            type_of_user="tutor",
        )

        self.student_user = Student.objects.create_user(
            username="student_user",
            password="password123",
            email="student_user@example.com",
            type_of_user="student",
        )

    def mock_view(self, request):
        return HttpResponse("Success")

    def test_admin_access(self):
        """Test that admin users can access the view."""
        request = self.factory.get("/test-path/")
        request.user = self.admin_user
        decorated_view = user_type_required("admin")(self.mock_view)
        response = decorated_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Success")

    def test_tutor_access(self):
        """Test that tutor users can access the view."""
        request = self.factory.get("/test-path/")
        request.user = self.tutor_user
        decorated_view = user_type_required("tutor")(self.mock_view)
        response = decorated_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Success")

    def test_student_access(self):
        """Test that student users can access the view."""
        request = self.factory.get("/test-path/")
        request.user = self.student_user
        decorated_view = user_type_required("student")(self.mock_view)
        response = decorated_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Success")

    def test_invalid_user_type(self):
        """Test that users with an incorrect type are redirected to unauthorized page."""
        request = self.factory.get("/test-path/")
        request.user = self.student_user
        decorated_view = user_type_required("tutor")(self.mock_view)
        response = decorated_view(request)
        self.assertEqual(response.status_code, 403)
        self.assertIn("Access Denied", response.content.decode())

    def test_anonymous_user(self):
        """Test that anonymous users are redirected to the unauthorized page."""
        request = self.factory.get("/test-path/")
        request.user = None
        decorated_view = user_type_required("admin")(self.mock_view)
        response = decorated_view(request)
        self.assertEqual(response.status_code, 403)
        self.assertIn("Access Denied", response.content.decode())

    def test_missing_type_of_user_attribute(self):
            """Test that users without the type_of_user attribute are redirected to unauthorized page."""
            user = User.objects.create_user(
                username="generic_user",
                password="password123",
                email="generic_user@example.com",
            )
            request = self.factory.get("/test-path/")
            request.user = user
            decorated_view = user_type_required("admin")(self.mock_view)
            response = decorated_view(request)
            self.assertEqual(response.status_code, 403)
            self.assertIn("Access Denied", response.content.decode())