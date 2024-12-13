from rest_framework import serializers
from .models import Lesson, Tutor


class LessonSerializer(serializers.ModelSerializer):       
    """
    serializer for the lesson model.
    validates and serializes the 'tutor' fiels.
    """
    
    class Meta: 
        """
        metadata for the LessonSerializer
        specifies the model and fields to include in the specialized output
        """
        model = Lesson
        fields = ['tutor']
    # custom validation method for the 'tutor' field
    # returns a string if validation passes
    def validate_tutor(self, value) -> str:
        # Ensure the value is not None or empty
        if not value:
            # raise validation error if the value is empty 
            raise serializers.ValidationError("Tutor is mandatory.")
        # If the value is a string (like whitespace), validate that it's not empty
        if isinstance(value, str) and not value.strip():
            raise serializers.ValidationError("Tutor cannot be whitespace.")
        # If the value is a Tutor object, allow it (typically happens in updates)
        if isinstance(value, Tutor):
            # return if the value is a valid Tutor object
            return value
        # return the validated value
        return value