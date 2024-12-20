
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar
from django.http import HttpRequest


class User(AbstractUser):
    """
    Model used for user authentication, and team member related information.
    """
    # vincent: Docstrings on 3 lines for better readibilty (remove these comments in final version)
    # vincent: TODO: change all Docstrings to multiple lines
    # vincent: TODO: remove spacings within functions

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

    def full_name(self) -> str:
        """Return a string containing the user's full name."""

        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120) -> str:
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self) -> str:
        """Return a URL to a miniature version of the user's gravatar."""
        
        return self.gravatar(size=60)

class Admin(User): 

    type_of_user = 'admin'

    def save(self, *args, **kwargs) -> None:
        self.is_staff = True
        self.superuser = True
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"Admin: {self.get_full_name()}"


class Tutor(User):  

    SUBJECTS = [ 
        ('ruby_on_rails', 'Ruby on Rails'),
        ('python', 'Python'),
        ('javascript', 'Javascript'),
        ('c_plus_plus', 'C++'),
        ('c_sharp', 'C#'),
        ('react', 'React'),
        ('angular', 'Angular'),
        ('vue_js', 'Vue_js'),
        ('node_js', 'Node_js'),
        ('express_js', 'Express_js'),
        ('django', 'Django'),
        ('flask', 'Flask'),
        ('spring', 'Spring'),
        ('hibernate', 'Hibernate'),
        ('jpa', 'JPA'),
        ('sql', 'Sql'),
        ('mongodb', 'MongoDB'),
        ('postgresql', 'PostgreSQL'),
        ('mysql', 'MySQL'),
        ('git', 'Git'),
    ]

    type_of_user = 'tutor'
    bio = models.CharField(max_length=520, blank=True, null=True)   # optional
    subjects = models.ManyToManyField('Subjects', related_name='tutors')    # multiple tutors can teach the same subject
    
    def __str__(self):
        return f"Tutor: {self.username} ({self.id})"


class Subjects(models.Model):  

    subject_name = models.CharField(max_length=100, unique=True)    
    timings = models.CharField(max_length=255, blank=True)
    bio = models.CharField(max_length=520, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    tutor_list = models.JSONField(default=list)

class Student(User):
    type_of_user = 'student'
    phone = models.CharField(max_length=12, default='07777777777')

class TutorAvailability(models.Model):   
    DAYS = [
        ('all', 'All'),  # Special value for availability on all days
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

class Invoice(models.Model):   
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)      # vincent: need this to make lesson acceptance, remove this comment in final version
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # vincent: need this to make lesson acceptance, remove this comment in final version
    orderNo = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=100, blank=False)       # vincent: need this to make lesson acceptance, remove this comment in final version
    no_of_classes = models.IntegerField(blank=False)           
    price_per_class = models.DecimalField(max_digits=10, decimal_places=2, blank=False, default=20)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, blank=False, default=0)

class Lesson(models.Model):  

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
        (120, '2 hours')
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

    PAYMENT_STATUS_CHOICES = [
        ('Unpaid', 'Unpaid'),
        ('Paid', 'Paid'),
    ]

    lesson_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='lessons')
    tutor = models.ForeignKey(Tutor, on_delete=models.SET_NULL, null=True, blank=True, related_name='lessons') 
    day_of_week = models.CharField(max_length=10, choices=DAYS)
    start_time = models.TimeField()
    duration = models.IntegerField(choices=DURATION_CHOICES, default=60)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    term = models.CharField(max_length=50, choices=TERMS)
    subject = models.CharField(max_length=100, choices=SUBJECTS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    invoice_no = models.ForeignKey(Invoice, null = True,on_delete=models.CASCADE)    
    payment_status = models.CharField(max_length=10,choices=PAYMENT_STATUS_CHOICES,default='Unpaid')
  
    

class Message(models.Model): 
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='messages')
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('resolved', 'Resolved')], default='pending')