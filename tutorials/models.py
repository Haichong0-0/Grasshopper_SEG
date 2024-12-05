
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

class Admin(User): # Deyu

    type_of_user = 'admin'

    # def save(self, *args, **kwargs):
    #     self.is_staff = True
    #     self.use_superuser = True
    #     super().save(*args, **kwargs)
    
    def __str__(self):
        # return (f"Admin: {self.user.full_name()}")
        return f"Admin: {self.get_full_name()}"


class Tutor(User):  

    type_of_user = 'tutor'
    bio = models.CharField(max_length=520, blank=True, null=True)

class Subjects(models.Model):  # George

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

    user = models.ForeignKey(User, on_delete=models.CASCADE,null = False)
    subject = models.CharField(max_length=100, choices=SUBJECTS)
    proficiency = models.CharField(max_length=12, choices=PROFICIENCY_LEVEL_CHOICES, default=INTERMEDIATE)

class Student(User):
    type_of_user = 'student'
    phone = models.CharField(max_length=12, default='07777777777')

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
    
    no_of_classes = models.IntegerField(blank=False)
    price_per_class = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    totalsum = models.DecimalField(max_digits=10, decimal_places=2, blank=False, default=0)
    
    def calc_sum(self):
        self.totalsum = self.no_of_classes * self.price_per_class
        return self.totalsum




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
        ('Rejected', 'Rejected'),
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('late', 'Late')
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
    day_of_week = models.CharField(max_length=10, choices=DAYS)
    start_time = models.TimeField()
    duration = models.IntegerField(choices=DURATION_CHOICES, default=60)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    term = models.CharField(max_length=50, choices=TERMS)

    subject = models.CharField(max_length=100, choices=SUBJECTS)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    invoiceNo = models.ForeignKey(Invoice, null = True,on_delete=models.CASCADE)


class Message(models.Model): #Arjan
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='messages')
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('resolved', 'Resolved')], default='pending')

 