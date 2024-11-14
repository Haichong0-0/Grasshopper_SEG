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




class Tutor(User):  # George
    SUBJECTS = [
        ('ruby_on_rails', 'Ruby on Rails'),
        ('python', 'Python'),
        ('javascript', 'Javascript'),
        ('c_plus_plus', 'C++'),
        ('c_sharp', 'C#'),
        ('react', 'React'),
        ('angular', 'Angular'),
        ('vue_js', 'Vue.js'),
        ('node_js', 'Node.js'),
        ('express_js', 'Express.js'),
        ('django', 'Django'),
        ('flask', 'Flask'),
        ('spring', 'Spring'),
        ('hibernate', 'Hibernate'),
        ('jpa', 'JPA'),
        ('sql', 'SQL'),
        ('mongodb', 'MongoDB'),
        ('postgresql', 'PostgreSQL'),
        ('mysql', 'MySQL'),
        ('git', 'Git'),
    ]
    
    tutorNo = models.AutoField(primary_key=True)          
    subject = models.CharField(max_length=100, blank=False,choices=SUBJECTS)
    bio = models.TextField(blank=True)

    
class Admin(): # Deyu



class Student(): # Arjan
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    preferred_language = models.CharField(max_length=50)
    preferred_tutor = models.ForeignKey('Tutor', on_delete=models.SET_NULL, null=True, blank=True)
    preferred_lesson_duration = models.IntegerField(default=60)
    preferred_lesson_frequency = models.CharField(max_length=20, choices=[('weekly', 'Weekly'), ('fortnightly', 'Fortnightly')])


    current_term_start_date = models.DateField(null=True, blank=True)
    current_term_end_date = models.DateField(null=True, blank=True)
    current_term_tutor = models.ForeignKey('Tutor', on_delete=models.SET_NULL, null=True, blank=True)
    current_term_lesson_time = models.TimeField(null=True, blank=True)



#class Lesson(): # Fatimah


#class Invoic(): # George
 
