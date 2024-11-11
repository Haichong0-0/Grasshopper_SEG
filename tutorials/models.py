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


class Tutor(User):  # George
    SUBJECTS = [("Ruby on Rails"), 
                ("Python"), 
                ("Javascript"), 
                ("C++"), 
                ("C#"), 
                ("React"), 
                ("Angular"), 
                ("Vue.js"), 
                ("Node.js"), 
                ("Express.js"), 
                ("Django"), 
                ("Flask"), 
                ("Spring"), 
                ("Hibernate"), 
                ("JPA"), 
                ("SQL"), 
                ("MongoDB"), 
                ("PostgreSQL"), 
                ("MySQL"), 
                ("Git")]
               
    subject = models.CharField(max_length=100, blank=False)
    timings = models.CharField(max_length=255, blank=True)

    def setTimings(self, timings_list):
        self.Timings = ','.join(timings_list)

    def getTimings(self):
        return self.Timings.split(',')



class Student(): # Arjan
    pass


class Lesson(): # Fatimah
    pass


class Invoic(models.Model): # George
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100, blank=False)
    no_of_classes = models.IntegerField(blank=False)
    price_per_class = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    sum = models.DecimalField(max_digits=10, decimal_places=2, blank=False)

    class Meta:
        def calculate_sum(self):
            self.sum = self.no_of_classes * self.price_per_class
            self.save()
        def getInvoice(self):
            return self.sum 