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
    date_of_birth = models.DateField(default='2000-01-01')

    USER_TYPES = (
        ('admin', 'Admin'),
        ('tutor', 'Tutor'),
        ('student', 'Student'),
    )

    type_of_user = models.CharField(max_length=20, choices=USER_TYPES, default='student')

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

class Admin(User):

    type_of_user = 'admin'

    def save(self, *args, **kwargs):
        self.user.is_staff = True
        self.user.use_superuser = True
        self.user.save()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return (f"Admin: {self.user.full_name()}")


class Tutor(User):  

    type_of_user = 'tutor'
    
    SUBJECTS = [ # All of the subjects that a Tutor is available to teach
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


    subject = models.CharField(max_length=100, blank=False, choices=SUBJECTS,default="Python")
    timings = models.CharField(max_length=255, blank=True)
    bio = models.CharField(max_length=520, blank=True, null=True)

    def setTimings(self, timings_list):
        self.Timings = ','.join(timings_list)

    def getTimings(self):
        return self.Timings.split(',')



class Student(User): #Arjun #Deyu

    type_of_user = 'student'
    
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


    current_term_start_date = models.DateField(null=True, blank=True) # student term time enrollment field details
    current_term_end_date = models.DateField(null=True, blank=True)
    current_term_tutor = models.ForeignKey(Tutor, on_delete=models.SET_NULL, null=True, blank=True, related_name='student_with_current_term_tutor')
    current_term_lesson_time = models.TimeField(null=True, blank=True)

class TutorAvailability():  # George
    tutorNo = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, blank=False)
    starttime = models.TimeField(blank=False)
    endtime = models.TimeField(blank=False)

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



""" class Invoice(models.Model):  # George
     orderNo = models.AutoField(primary_key=True)
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
             return self.sum  """
 
