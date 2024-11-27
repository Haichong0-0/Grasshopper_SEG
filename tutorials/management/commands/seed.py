from django.core.management.base import BaseCommand, CommandError
from tutorials.models import User, Tutor, Student, Admin
import pytz
from faker import Faker
from random import choice

user_fixtures = [
    {'username': '@johndoe', 'email': 'john.doe@example.org', 'first_name': 'John', 'last_name': 'Doe'},
    {'username': '@janedoe', 'email': 'jane.doe@example.org', 'first_name': 'Jane', 'last_name': 'Doe'},
    {'username': '@charlie', 'email': 'charlie.johnson@example.org', 'first_name': 'Charlie', 'last_name': 'Johnson'},
]

admin_fixtures = [
    {'username': '@admin', 'email': 'admin.admin@example.org', 'first_name': 'Admin', 'last_name': 'Admin'},
    {'username': '@SteveJobs', 'email': 'Steve.Jobs@example.org', 'first_name': 'Steve', 'last_name': 'Jobs'},
]

tutor_fixtures = [
    {'username': '@tutor', 'email': 'tutor@example.org', 'first_name': 'Tutor', 'last_name': 'Tutor', 'subject': 'ruby_on_rails'},
    {'username': '@jeroenkeppens', 'email': 'jeroen.keppens@example.org', 'first_name': 'Jeroen', 'last_name': 'Keppens', 'subject': 'python'},
]

student_fixtures = [
    {'username': '@student', 'email': 'student@example.org', 'first_name': 'Student', 'last_name': 'Student', 'proficiency_level': 'beginner'},
]


lesson_fixtures = [
    {Student:'@johndoe','tutor':'@tutor','lesson_time':'2021-01-01 12:00:00','lesson_duration':60},

] 




class Command(BaseCommand):
    """Build automation command to seed the database."""

    TUTOR_COUNT = 5
    STUDENT_COUNT = 20
    ADMIN_COUNT = 10
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        #self.create_users()
        self.create_tutors()
        self.create_admins()
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
            self.try_create_user(self.generate_user())
            user_count = User.objects.count()
        print("User seeding complete.      ")

    def generate_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        data = {'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name}
        return data
        #return self.try_create_user({'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name})

    def try_create_user(self, data):
        try:
            return self.create_user(data)
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    def create_user(self, data):
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
        )
        return user


    def create_students(self):
        student_count = Student.objects.count()
        while student_count < self.STUDENT_COUNT:
            print(f"Seeding Student {student_count}/{self.STUDENT_COUNT}", end='\r')
            data = self.generate_user()
            if data:
                self.try_create_student(data)
            student_count = Student.objects.count()
        print("student seeding complete.      ")

    def create_tutors(self):
        tutor_count = Tutor.objects.count()
        self.create_tutor_fixtures()
        while tutor_count < self.TUTOR_COUNT:
            print(f"Seeding Tutor {tutor_count}/{self.TUTOR_COUNT}", end='\r')
            data = self.generate_user()
            if data:
                self.try_create_tutor(data)
            tutor_count = Tutor.objects.count()
        print("Tutor seeding complete.      ")

    def create_tutor_fixtures(self):
        for data in tutor_fixtures:
            self.try_create_tutor(data)

    def create_admins(self):
        for data in admin_fixtures:
            self.try_create_admin(data)
        print(f"Admin seeding complete.      ")


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

    def try_create_admin(self, data):
        try:
            return self.generate_admin(data)
        except Exception as e:
            print(f"Error creating admin: {e}")
            return None

    def generate_tutor(self, data):
        subject = choice([ subject[0] for subject in Tutor.SUBJECTS])
        if(len(data)>4):
            subject = data['subject']
        Tutor.objects.create(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
            subject=subject,
            bio=self.faker.text(),
        )

    def generate_admin(self, data):
        admin = Admin.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
        )
        return admin
    
    def generate_student(self, data):
        proficiency_level = choice([Student.BEGINNER, Student.NOVICE, Student.INTERMEDIATE, Student.ADVANCED, Student.MASTERY])
        preferred_language = choice(["Python", "Java", "JavaScript", "C++", "Ruby"])
        preferred_frequency = choice(['weekly', 'fortnightly'])
        preferred_tutor = None
        phone = "07777777777" 
        student = Student.objects.create(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
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