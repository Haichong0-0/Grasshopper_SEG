from rest_framework import serializers
from .models import Lesson 

class LessonSerializer(serializers.ModelSerializer):
    class Meta: 
        model= Lesson

        # fields = ['subject', 'tutor', 'frequency', 'duration', 'start_date', 'day_of_week', 'start_time', 'term', 'location' ]
        fields = ['tutor']
        
    def validate_tutor(self, value):
        print("printing value: ", value)
        if not value:
            raise serializers.ValidationError("Tutor is mandatory.")
        return value
