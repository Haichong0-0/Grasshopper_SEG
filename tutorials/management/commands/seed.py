from django.core.management.base import BaseCommand, CommandError
from tutorials.models import User, Tutor, Student
import pytz
from faker import Faker
from random import choice

user_fixtures = [
    {'username': '@johndoe', 'email': 'john.doe@example.org', 'first_name': 'John', 'last_name': 'Doe'},
    {'username': '@janedoe', 'email': 'jane.doe@example.org', 'first_name': 'Jane', 'last_name': 'Doe'},
    {'username': '@charlie', 'email': 'charlie.johnson@example.org', 'first_name': 'Charlie', 'last_name': 'Johnson'},
]

class Command(BaseCommand):
    """Build automation command to seed the database."""

    USER_COUNT = 300
    TUTOR_COUNT = 30
    STUDENT_COUNT = 30
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_tutors()
        self.create_users()
        self.create_students()
        
        self.users = User.objects.all()

    def create_users(self):
        self.generate_user_fixtures()
        self.generate_random_users()

    def generate_user_fixtures(self):
        for data in user_fixtures:
            self.try_create_user(data)

    def generate_random_users(self):
        user_count = User.objects.count()
        while user_count < self.USER_COUNT:
            print(f"Seeding user {user_count}/{self.USER_COUNT}", end='\r')
            self.generate_user()
            user_count = User.objects.count()
        print("User seeding complete.      ")

    def generate_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        return self.try_create_user({'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name})

    def try_create_user(self, data):
        try:
            return self.create_user(data)
        except:
            pass

    def create_user(self, data):
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
        )
        return user

    def create_tutors(self):
        tutor_count = Tutor.objects.count()
        while tutor_count < self.TUTOR_COUNT:
            print(f"Seeding Tutor {tutor_count}/{self.TUTOR_COUNT}", end='\r')
            user = self.generate_user()
            if user:
                self.try_create_tutor(user)
            tutor_count = Tutor.objects.count()
        print("Tutor seeding complete.      ")
    
    def create_students(self):
        student_count = Student.objects.count()
        while student_count < self.STUDENT_COUNT:
            print(f"Seeding Student {student_count}/{self.STUDENT_COUNT}", end='\r')
            user = self.generate_user()
            if user:
                self.try_create_student(user)
            student_count = Student.objects.count()
        print("student seeding complete.      ")

    def try_create_tutor(self, user):
        try:
            self.generate_tutor(user)
        except Exception as e:
            print(f"Error creating tutor: {e}")

    def try_create_student(self, user):
        try:
            self.generate_student(user)
        except Exception as e:
            print(f"Error creating students: {e}")

    def generate_tutor(self, user):
        subject = choice([subject[0] for subject in Tutor.SUBJECTS])
        un = user.username
        mail = user.email
        pw = user.password
        fn = user.first_name
        lastn = user.last_name
        user.delete()
        Tutor.objects.create(
            username=un,
            email=mail,
            password=pw,
            first_name=fn,
            last_name=lastn,
            subject=subject,
            bio=self.faker.text(),
        )
    
    def generate_student(self, user):
        proficiency_level = choice([Student.BEGINNER, Student.NOVICE, Student.INTERMEDIATE, Student.ADVANCED, Student.MASTERY])
        preferred_language = choice(["Python", "Java", "JavaScript", "C++", "Ruby"])
        preferred_frequency = choice(['weekly', 'fortnightly'])
        preferred_tutor = None
        un = user.username
        mail = user.email
        pw = user.password
        fn = user.first_name
        lastn = user.last_name
        phone = "07777777777" 
        user.delete()
        student = Student.objects.create(
            username=un,
            email=mail,
            password=pw,
            first_name=fn,
            last_name=lastn,
            proficiency_level=proficiency_level,
            phone=phone,
            preferred_language=preferred_language,
            preferred_tutor=preferred_tutor,
            preferred_lesson_duration=60,
            preferred_lesson_frequency=preferred_frequency,
            current_term_start_date=None,
            current_term_end_date=None,
            current_term_tutor=None,
            current_term_lesson_time=None,
        )


def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()

def create_email(first_name, last_name):
    return first_name + '.' + last_name + '@example.org'