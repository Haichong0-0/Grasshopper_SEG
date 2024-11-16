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

    # # Student-specific fields (nullable for other roles)
    # BEGINNER = 'Beginner'
    # NOVICE = 'Novice'
    # INTERMEDIATE = 'Intermediate'
    # ADVANCED = 'Advanced'
    # MASTERY = 'Mastery'
    # PROFICIENCY_LEVEL_CHOICES = [
    #     (BEGINNER, 'Beginner'),
    #     (NOVICE, 'Novice'),
    #     (INTERMEDIATE, 'Intermediate'),
    #     (ADVANCED, 'Advanced'),
    #     (MASTERY, 'Mastery'),
    # ]
    # proficiency_level = models.CharField(
    #     max_length=12,
    #     choices=PROFICIENCY_LEVEL_CHOICES,
    #     default=NOVICE,
    #     blank=True,
    #     null=True
    # )


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


class Tutor(User):  # George # Deyu
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
    
    tutorNo = models.AutoField(primary_key=True, default='1')           
    subject = models.CharField(max_length=100, blank=False, default="Python")
    timings = models.CharField(max_length=255, blank=True)
    bio = models.CharField(max_length=520, blank=True, null=True)

    def setTimings(self, timings_list):
        self.Timings = ','.join(timings_list)

    def getTimings(self):
        return self.Timings.split(',')



class Student(User): # Arjan # Deyu

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

class TutorAvailability():  # George
    tutorNo = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, blank=False)
    starttime = models.TimeField(blank=False)
    endtime = models.TimeField(blank=False)

#class Lesson(): # Fatimah


# class Invoice(models.Model):  # George
#     orderNo = models.AutoField(primary_key=True)
#     tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     topic = models.CharField(max_length=100, blank=False)
#     no_of_classes = models.IntegerField(blank=False)
#     price_per_class = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
#     sum = models.DecimalField(max_digits=10, decimal_places=2, blank=False)

#     class Meta:
#         def calculate_sum(self):
#             self.sum = self.no_of_classes * self.price_per_class
#             self.save()
#         def getInvoice(self):
#             return self.sum 
 
