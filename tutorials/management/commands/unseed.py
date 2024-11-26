from django.core.management.base import BaseCommand, CommandError
from tutorials.models import User,Tutor,Student,Admin

class Command(BaseCommand):
    """Build automation command to unseed the database."""
    
    help = 'Seeds the database with sample data'

    def handle(self, *args, **options):
        """Unseed the database."""
        Tutor.objects.all().delete()
        Student.objects.all().delete()
        Admin.objects.all().delete()
        User.objects.filter(is_staff=False).delete()