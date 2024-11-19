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

    
#class Admin(): # Deyu


#class Tutor(): # George


class Student(): # Arjan
    BEGINNER = 'Beginner'
    NOVICE = 'Novice'
    INTERMEDIATE = 'Intermediate'
    ADVANCED = 'Advanced'
    MASTERY = 'Mastery'
    PROFICIENCY_LEVEL_CHOICES = [
        (BEGINNER, 'Beginner'),
        (NOVICE, 'Novice'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced'),
        (MASTERY, 'Mastery'),
    ]
    proficiency_level = models.CharField(
        max_length=12,
        choices=PROFICIENCY_LEVEL_CHOICES,
        default=INTERMEDIATE,
        blank=True,
        null=True
    )

    phone = models.CharField(max_length=12, default='07777777777')

    preferred_language = models.CharField(max_length=50, default="Python")
    preferred_tutor = models.ForeignKey(Tutor, on_delete=models.SET_NULL, null=True, blank=True, related_name='student_preferring_tutor')
    preferred_lesson_duration = models.IntegerField(default=60)
    preferred_lesson_frequency = models.CharField(max_length=20, choices=[('weekly', 'Weekly'), ('fortnightly', 'Fortnightly')], default="('weekly', 'Weekly')")


    current_term_start_date = models.DateField(null=True, blank=True)
    current_term_end_date = models.DateField(null=True, blank=True)
    current_term_tutor = models.ForeignKey(Tutor, on_delete=models.SET_NULL, null=True, blank=True, related_name='student_with_current_term_tutor')
    current_term_lesson_time = models.TimeField(null=True, blank=True)


class Lesson(models.Model): #Fatimah

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

    FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('fortnightly', 'Fortnightly'),
        ('every other week', 'Every other week')
    ]
    
    DURATION_CHOICES = [
        (60, '1 hour'),
        (120, '2 hours'),
    ]

    TERMS = [
        ('September-Christmas', 'September-Christmas'),
        ('January-Easter term','January-Easter' ),
        ('May-July','May-July')
    ]


    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed')
    ]

    TIME_CHOICES = [
        ('09:00', '9:00 AM'),
        ('10:00', '10:00 AM'),
        ('11:00', '11:00 AM'),
        ('12:00', '12:00 PM'),
        ('13:00', '1:00 PM'),
        ('14:00', '2:00 PM'),
        ('15:00', '3:00 PM'),
        ('16:00', '4:00 PM'),
        ('17:00', '5:00 PM'),
    ]

    DAYS = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='lessons')
    tutor = models.ForeignKey(Tutor, on_delete=models.SET_NULL, null=True, blank=True, related_name='lessons')
    subject = models.CharField(max_length=100, choices=SUBJECTS)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    term = models.CharField(max_length=50, choices=TERMS)
    duration = models.IntegerField(choices=DURATION_CHOICES, default=60)
    start_date = models.DateField()
    day_of_week = models.CharField(max_length=10, choices=DAYS)
    start_time = models.CharField(max_length=5, choices=TIME_CHOICES, default='09:00')
    location = models.CharField(max_length=100, default="Online") 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    invoice_paid = models.BooleanField(default=False)
    price_per_term = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

#class Invoic(): # George