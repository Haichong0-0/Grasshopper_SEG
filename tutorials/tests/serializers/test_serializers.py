"""Unit tests of the user form."""
from tutorials.models import Admin, Tutor, Student
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from tutorials.serializer import LessonSerializer

class LessonSerializerTestCase(TestCase):

# created with the help of chatGPT

    def setUp(self):
        self.admin = Admin.objects.create_user(
            username="adminuser",
            password="password123",
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
            type_of_user='admin'
        )

        self.tutor = Tutor.objects.create(
            username="tutoruser",
            password="password123",
            first_name="Tutor",
            last_name="User",
            email="tutor@example.com",
            date_of_birth="1985-05-15"
        )

        self.student = Student.objects.create(
            username="studentuser",
            password="password123",
            first_name="Student",
            last_name="User",
            email="student@example.com",
            date_of_birth="2005-07-10"
        )

        # Define valid and invalid data for testing
        self.valid_data = {
            'tutor': self.tutor.id,
        }

        self.invalid_data_missing_tutor = {
            # Missing the 'tutor' field
        }

        self.invalid_data_invalid_tutor = {
            'tutor': 99999  # Non-existent tutor ID
        }

    def test_valid_tutor(self):
        """Test serializer with valid tutor data."""
        valid_data = self.valid_data.copy()
        serializer = LessonSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid(), msg=f"Errors: {serializer.errors}")
        # Compare the `Tutor` object directly, as the serializer resolves the ID to an object
        self.assertEqual(serializer.validated_data['tutor'], self.tutor)

    def test_validate_tutor_with_whitespace(self):
        serializer = LessonSerializer(data={'tutor': '   '})  # Whitespace input
        self.assertFalse(serializer.is_valid())
        self.assertIn('tutor', serializer.errors)
        self.assertEqual(serializer.errors['tutor'][0], "Tutor cannot be whitespace.")

    def test_validate_tutor_with_whitespace(self):
        # Test whitespace validation with tutor ID (primary key)
        serializer = LessonSerializer(data={'tutor': '   '})
        with self.assertRaises(ValidationError):
            serializer.validate_tutor("   ")  # Whitespace-only input

    def test_tutor_with_invalid_data_type(self):
        data = {'tutor': 12345}  # Invalid data type for tutor
        serializer = LessonSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('tutor', serializer.errors)

    def test_serializer_fields(self):
        serializer = LessonSerializer()
        self.assertEqual(set(serializer.Meta.fields), {'tutor'})

    def test_validate_tutor_with_whitespace(self):
        serializer = LessonSerializer()
        with self.assertRaises(ValidationError):
            serializer.validate_tutor("   ")  # Whitespace-only input

    def test_valid_data(self):
        """Test serializer with valid data."""
        serializer = LessonSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), msg=f"Errors: {serializer.errors}")
        self.assertEqual(serializer.validated_data['tutor'], self.tutor)

    def test_missing_tutor_field(self):
        """Test serializer with missing tutor field."""
        serializer = LessonSerializer(data={})  # No tutor field provided
        self.assertTrue(serializer.is_valid(), msg=f"Serializer should be valid: {serializer.errors}")
        self.assertNotIn('tutor', serializer.validated_data, msg="Tutor field should not be in validated data when missing.")

    def test_invalid_tutor_id(self):
        """Test serializer with invalid tutor ID."""
        serializer = LessonSerializer(data=self.invalid_data_invalid_tutor)
        self.assertFalse(serializer.is_valid())
        self.assertIn('tutor', serializer.errors)
        self.assertEqual(serializer.errors['tutor'][0], "Invalid pk \"99999\" - object does not exist.")

    def test_whitespace_tutor(self):
        """Test serializer with whitespace as tutor."""
        serializer = LessonSerializer(data={'tutor': '   '})
        self.assertFalse(serializer.is_valid(), msg=f"Unexpectedly valid data: {serializer.validated_data}")
        self.assertIn('tutor', serializer.errors, msg=f"Errors: {serializer.errors}")
        self.assertEqual(
            str(serializer.errors['tutor'][0]),
            "Incorrect type. Expected pk value, received str."
        )

    def test_direct_validate_tutor(self):
        """Test the validate_tutor method directly."""
        serializer = LessonSerializer()

        # Valid tutor
        self.assertEqual(serializer.validate_tutor(self.tutor), self.tutor)

        # Invalid (None)
        with self.assertRaises(ValidationError) as context:
            serializer.validate_tutor(None)
        self.assertEqual(context.exception.detail[0], "Tutor is mandatory.")

        # Invalid (whitespace)
        with self.assertRaises(ValidationError) as context:
            serializer.validate_tutor("   ")
        self.assertEqual(context.exception.detail[0], "Tutor cannot be whitespace.")

    def test_serializer_fields(self):
        """Test the fields included in the serializer."""
        serializer = LessonSerializer()
        self.assertEqual(set(serializer.Meta.fields), {'tutor'})

    def test_validate_tutor_with_valid_tutor_object(self):
        """Test validate_tutor with a valid Tutor object."""
        serializer = LessonSerializer()
        result = serializer.validate_tutor(self.tutor)  # Pass a Tutor object
        self.assertEqual(result, self.tutor, "The validate_tutor method should return the valid Tutor object.")

    def test_validate_tutor_with_valid_pk(self):
        """Test validate_tutor with a valid primary key (pk)."""
        serializer = LessonSerializer(data={'tutor': self.tutor.id})
        self.assertTrue(serializer.is_valid(), msg=f"Errors: {serializer.errors}")
        self.assertEqual(serializer.validated_data['tutor'], self.tutor, "The tutor should resolve to the Tutor object.")

    def test_validate_tutor_direct_object(self):
        """Test validate_tutor directly with a Tutor object."""
        serializer = LessonSerializer()
        validated_tutor = serializer.validate_tutor(self.tutor)
        self.assertEqual(validated_tutor, self.tutor, "The method should return the Tutor object as is.")

    def test_validate_tutor_with_valid_id(self):
        """Test validate_tutor with a valid primary key."""
        serializer = LessonSerializer(data={'tutor': self.tutor.id})
        self.assertTrue(serializer.is_valid(), msg=f"Errors: {serializer.errors}")
        self.assertEqual(serializer.validated_data['tutor'], self.tutor, "The tutor should resolve to the Tutor object.")

    def test_validate_tutor_with_other_valid_value(self):
        """Test validate_tutor with a valid non-Tutor object."""
        serializer = LessonSerializer()
        # Simulate a valid value not covered by previous conditions
        value = "SomeOtherValidValue"
        result = serializer.validate_tutor(value)
        # Assert that the value is returned unchanged
        self.assertEqual(result, value, "The validate_tutor method should return the value unchanged.")
