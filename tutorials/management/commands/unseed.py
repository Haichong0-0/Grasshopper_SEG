from django.core.management.base import BaseCommand, CommandError
from tutorials.models import *

class Command(BaseCommand):
    """Build automation command to unseed the database."""
    
    help = 'Seeds the database with sample data'

    def handle(self, *args, **options):
        """Unseed the database."""
        try:
            Tutor.objects.all().delete()
            Student.objects.all().delete()
            Admin.objects.all().delete()
            Lesson.objects.all().delete()  
            TutorAvailability.objects.all().delete()
            Invoice.objects.all().delete()
            User.objects.filter(is_staff=False).delete()
            print("Unseed successfully. All relevant data has been removed.")
        except Exception as e:
            print(f"An error occurred while unseeding: {e}")