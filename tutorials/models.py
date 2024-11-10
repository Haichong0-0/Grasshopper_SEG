from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar

class User(AbstractUser):
    """Model used for user authentication, and team member related information."""

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)


    class Meta:
        """Model options."""

        ordering = ['last_name', 'first_name']

    def full_name(self):
        """Return a string containing the user's full name."""

        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        
        return self.gravatar(size=60)
    
class Admin(): # Deyu
    pass
    
class Tutor(): # George
    pass


class Student(): # Arjan
    pass
    
class Lesson(models.Model): #Fatimah
    FREQUENCY_CHOICES = [
        ('weekly'),
        ('fortnightly'),
        ('every other week')
    ]
    
    DURATION_CHOICES = [
        (60, '1 hour'),
        (120, '2 hours'),
    ]

    TERMS = [
        ('September-Christmas'),
        ('January-Easter term'),
        ('May-July')
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='lessons')
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='lessons')
    subject = models.CharField(max_length=100)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    term = models.CharField(max_length=50, choices=TERMS)
    duration = models.IntegerField(choices=DURATION_CHOICES, default=60)
    start_date = models.DateField()
    day_of_week = models.CharField(max_length=10, choices=[
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ])
    start_time = models.TimeField()
    location = models.CharField(max_length=100, default="Online") 
    is_approved = models.BooleanField(default=False)
    invoice_paid = models.BooleanField(default=False)
    price_per_term = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)


class Invoic(): # George
    pass
 
