
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
        self.is_staff = True
        self.use_superuser = True
        super().save(*args, **kwargs)
    
    def __str__(self):
        return (f"Admin: {self.get_full_name()}")


class Tutor(User):  

    type_of_user = 'tutor'
    
    


    subject = models.CharField(max_length=100, blank=False, choices=User.SUBJECTS,default="Python")
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


    preferred_language = models.CharField(max_length=50, default="Python", choices=User.SUBJECTS)
    preferred_tutor = models.ForeignKey(Tutor, on_delete=models.SET_NULL, null=True, blank=True, related_name='student_preferring_tutor')
    preferred_lesson_duration = models.IntegerField(default=60)
    preferred_lesson_frequency = models.CharField(max_length=20, choices=[('weekly', 'Weekly'), ('fortnightly', 'Fortnightly')], default="('weekly', 'Weekly')")
    current_term_start_date = models.DateField(null=True, blank=True)
    current_term_end_date = models.DateField(null=True, blank=True)
    current_term_tutor = models.ForeignKey(Tutor, on_delete=models.SET_NULL, null=True, blank=True, related_name='student_with_current_term_tutor')
    current_term_lesson_time = models.TimeField(null=True, blank=True)

class TutorAvailability(models.Model):  # George
    DAYS = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, blank=False, choices=DAYS)
    starttime = models.TimeField(blank=False)
    endtime = models.TimeField(blank=False)

class Invoice(models.Model):  # George
    orderNo = models.AutoField(primary_key=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE,)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    no_of_classes = models.IntegerField(blank=False)
    price_per_class = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    sum = models.DecimalField(max_digits=10, decimal_places=2, blank=False)

    def sum(self):
        self.sum = self.no_of_classes * self.price_per_class
        return self.sum

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
        ('January-Easter','January-Easter' ),
        ('May-July','May-July')
    ]


    STATUS_CHOICES = [
        ('Rejected', 'Rejected'),
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('late', 'Late')
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
    subject = models.CharField(max_length=100, choices=SUBJECTS,default="Python")
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    term = models.CharField(max_length=50, choices=TERMS)
    duration = models.IntegerField(choices=DURATION_CHOICES, default=60)
    start_date = models.DateField(null=True, blank=True)
    day_of_week = models.CharField(max_length=10, choices=DAYS)
    start_time = models.CharField(max_length=5, choices=TIME_CHOICES, default='09:00')
    location = models.CharField(max_length=100, default="Online") 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    invoice_paid = models.BooleanField(default=False)
    invoice = models.ForeignKey(Invoice, null = True,on_delete=models.CASCADE)



 