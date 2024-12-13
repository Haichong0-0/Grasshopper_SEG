from django.core.management.base import BaseCommand, CommandError
from tutorials.models import *
import pytz
from faker import Faker
import random
from tutorials.models import Subjects, Tutor 

user_fixtures = [         
    {'username': '@oliviabrown', 'email': 'olivia.brown@example.org', 'first_name': 'Olivia', 'last_name': 'Brown'},
    {'username': '@lucaswilliams', 'email': 'lucas.williams@example.org', 'first_name': 'Lucas', 'last_name': 'Williams'},
    {'username': '@elijahdavis', 'email': 'elijah.davis@example.org', 'first_name': 'Elijah', 'last_name': 'Davis'},
]

admin_fixtures = [
    {'username': '@admin', 'email': 'admin.admin@example.org', 'first_name': 'Admin', 'last_name': 'Admin'},
    {'username': '@johndoe', 'email': 'johndoe@example.org', 'first_name': 'John', 'last_name': 'Doe'},
]

tutor_fixtures = [
    {'username': '@tutor', 'email': 'tutor@example.org', 'first_name': 'Tutor', 'last_name': 'Tutor'},
    {'username': '@janedoe', 'email': 'janedoe@example.org', 'first_name': 'Jane', 'last_name': 'Doe'},
]

student_fixtures = [
    {'username': '@student', 'email': 'student@example.org', 'first_name': 'Student', 'last_name': 'Student'},  
    {'username': '@charlie', 'email': 'charlie@example.org', 'first_name': 'charlie', 'last_name': 'Student'},
]

tutor_availability_fixtures = [
    {'tutor':'@tutor', 'day':'monday', 'starttime':'10:00', 'endtime':'12:00'},
    {'tutor':'@tutor', 'day':'tuesday', 'starttime':'15:00', 'endtime':'17:00'},
    {'tutor':'@tutor', 'day':'wednesday', 'starttime':'10:00', 'endtime':'12:00'},
    {'tutor':'@tutor', 'day':'thursday', 'starttime':'15:00', 'endtime':'17:00'},
    {'tutor':'@tutor', 'day':'friday', 'starttime':'10:00', 'endtime':'12:00'},
    {'tutor':'@tutor', 'day':'saturday', 'starttime':'15:00', 'endtime':'17:00'},
    {'tutor':'@tutor', 'day':'sunday', 'starttime':'10:00', 'endtime':'12:00'},
    {'tutor':'@jeroenkeppens', 'day':'monday', 'starttime':'10:00', 'endtime':'12:00'},
    {'tutor':'@jeroenkeppens', 'day':'tuesday', 'starttime':'15:00', 'endtime':'17:00'},
    {'tutor':'@jeroenkeppens', 'day':'wednesday', 'starttime':'10:00', 'endtime':'12:00'},
    {'tutor':'@jeroenkeppens', 'day':'thursday', 'starttime':'15:00', 'endtime':'17:00'},
    {'tutor':'@jeroenkeppens', 'day':'friday', 'starttime':'10:00', 'endtime':'12:00'},
    {'tutor':'@jeroenkeppens', 'day':'saturday', 'starttime':'15:00', 'endtime':'17:00'},
    {'tutor':'@jeroenkeppens', 'day':'sunday', 'starttime':'10:00', 'endtime':'12:00'},
]

subject_fixtures = [
    {'user':'@tutor','subject':'Ruby_on_rails','proficiency':'Intermediate'},
]

# subject_names = [     # used in create subject fixtures, use the below one to match populate_subjects method
#     'Python', 'Django', 'React', 'JavaScript', 'SQL', 
#     'C++', 'C#', 'Node.js', 'Flask', 'Spring'
# ]

subject_names = [
    'Ruby_on_rails', 'python', 'javascript', 'c_plus_plus', 'c_sharp', 
    'react', 'angular', 'vue_js', 'node_js', 'express_js', 
    'django', 'flask', 'spring', 'hibernate', 'jpa', 
    'sql', 'mongodb', 'postgresql', 'mysql', 'git'
]



lesson_fixtures = [
    {'student':'@student',
     'tutor':'@tutor',
     'subject':'Ruby_on_rails',
     'frequency':'weekly',
     'terms':'September-Christmas',
     'duration':60,
    'day_of_week':'monday',
    'start_time':'10:00',
    'status':'Confirmed',
    'invoice': 0,
     },

     {'student':'@charlie',
      'tutor':'@janedoe',
      'subject':'Python',
      'frequency':'fortnightly',
      'terms':'January-Easter',
      'duration':60,
      'day_of_week':'tuesday',
      'start_time':'15:00',
      'status':'Confirmed',
      'invoice': 1,},
] 

invoice_fixtures = [
    {   'no_of_classes' : 10,
        'price_per_class' : 20,},
    {   'no_of_classes' : 6,
        'price_per_class' : 20,},
]

class Command(BaseCommand):
    """Build automation command to seed the database."""
    TUTOR_COUNT = 100
    STUDENT_COUNT = 50
    SUBJECT_COUNT =10
    ADMIN_COUNT = 10
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        populate_subjects()
        self.create_tutors()
        self.generate_tutor_availability()      # initially all tutors are free
        self.create_admins()
        self.create_students()
        self.generate_lesson_fixtures()      # creating errors
        self.users = User.objects.all()

    def create_users(self):
        self.generate_user_fixtures()
        self.generate_random_users()

    def generate_user_fixtures(self):
        for data in user_fixtures:
            self.try_create_user(data)
    
    def create_subject_fixtures(self):
        for subject_name in subject_names:
            self.try_create_subject(subject_name)

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
        self.create_student_fixtures()
        while student_count < self.STUDENT_COUNT:
            print(f"Seeding Student {student_count}/{self.STUDENT_COUNT}", end='\r')
            data = self.generate_user()
            if data:
                self.try_create_student(data)
            student_count = Student.objects.count()
        print("student seeding complete.      ")

    def create_student_fixtures(self):
        for data in student_fixtures:
            self.try_create_student(data)

    def create_subjects(self):
        subject_count = Subjects.objects.count()
        generated_subjects = 0
        while subject_count < self.SUBJECT_COUNT:
            generated_subjects = random.randint(0, len(subject_names)-1)
            subject_name = subject_names[generated_subjects]              
            self.try_create_subject({"subject_name": subject_name})
            subject_count = Subjects.objects.count()
        print("Subjects seeding complete.      ")

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

    def try_create_student(self, data):
        try:
            self.generate_student(data)
        except Exception as e:
            print(f"Error creating students: {e}")

    def try_create_subject(self, subject_name):
        try:
            self.generate_subject(subject_name)
        except Exception as e:
            print(f"Error creating subject: {e}")

    def try_create_admin(self, data):
        try:
            return self.generate_admin(data)
        except Exception as e:
            print(f"Error creating admin: {e}")
            return None

    def generate_tutor(self, data):
        all_subjects = list(Subjects.objects.all())
        selected_subjects = random.sample(all_subjects, 3)
        tutor = Tutor.objects.create(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
            bio=self.faker.text(),
            type_of_user = 'tutor',
        )
        tutor.set_password(Command.DEFAULT_PASSWORD)  # hashes the password
        tutor.save()
        tutor.subjects.add(*selected_subjects)
        for subjects in selected_subjects:
            subjects.tutor_list.append(tutor.username)
            subjects.save()

    def generate_admin(self, data):
        admin = Admin.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
            type_of_user = 'admin'
        )
        return admin
    
    def generate_student(self, data):
        """ proficiency_level = choice([Student.BEGINNER, Student.NOVICE, Student.INTERMEDIATE, Student.ADVANCED, Student.MASTERY])
        preferred_language = choice(["Python", "Java", "JavaScript", "C++", "Ruby"])
        preferred_frequency = choice(['weekly', 'fortnightly'])
        preferred_tutor = None """
        phone = "07777777777" 
        student = Student.objects.create(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=phone,
        )
        student.set_password(Command.DEFAULT_PASSWORD)  # This hashes the password
        student.save()

    def generate_subject(self, data):
        default_timings = "Monday-Friday, 9AM-5PM"
        default_bio = f"{data['subject_name']} is a core subject offered by our selected tutors."
        subject = Subjects.objects.create(
            subject_name=data['subject_name'],
            timings=data.get('timings', default_timings), 
            bio=data.get('bio', default_bio),  
        )
        subject.save()
        return subject

    def generate_lesson_fixtures(self):           # creating errors
        for data in lesson_fixtures:
            try:
                student = Student.objects.get(username=data['student'])  # Get Student instance
                tutor = Tutor.objects.get(username=data['tutor'])  # Get Tutor instance
                # subject = Subjects.objects.get(subject_name=data['subject'])  # Get Subject instance
                invoice = self.try_create_invoice(invoice_fixtures[data['invoice']], student, tutor)
                Lesson.objects.create(
                    student=student,
                    tutor=tutor,
                    subject=['subject'],
                    frequency=data['frequency'],
                    term=data['terms'],
                    duration=data['duration'],
                    day_of_week=data['day_of_week'],
                    start_time=data['start_time'],
                    status=data['status'],
                    invoice_no=invoice,
                )
                print(f"Lesson created: {data['student']} with {data['tutor']} for {data['subject']}")
            except Exception as e:
                print(f"Error creating lesson: {e}")

    def generate_tutor_availability(self):
        tutors = Tutor.objects.all()
        for tutor in tutors:
            TutorAvailability.objects.create(
                tutor=tutor,
                day='all',          # initially free on all days
                starttime='00:00',  # Start of the day
                endtime='23:59'     # End of the day
            )

    def try_create_invoice(self, data, student, tutor):
        try:
            return self.create_invoice(data, student, tutor)
        except Exception as e:
            print(f"Error creating invoice: {e}")
            return None
    
    def create_invoice(self, data, student, tutor):
        invoice = Invoice.objects.create(
            no_of_classes=data['no_of_classes'],
            price_per_class=data['price_per_class'],
            student=student,
            tutor=tutor
        )
        invoice.calc_sum()
        return invoice

    def create_lesson(self, data):
        invoice = self.try_create_invoice(invoice_fixtures[data['invoice']])
        student = Student.objects.get(username=data['student'])
        tutor = Tutor.objects.get(username=data['tutor'])
        lesson = Lesson.objects.create(
            student=student,
            tutor=tutor,
            subject=data['subject'],
            frequency=data['frequency'],
            term=data['terms'],
            duration=data['duration'],
            day_of_week=data['day_of_week'],
            start_time=data['start_time'],
            status=data['status'],
            # invoiceNo=invoice,
            invoice=invoice,
        )
        return lesson

    def create_tutor_availability(self, data):
        tutor = Tutor.objects.get(username=data['tutor'])
        tutor_availability = TutorAvailability.objects.create(
            tutor=tutor,
            day=data['day'],
            starttime=data['starttime'],
            endtime=data['endtime'],
        )
        return tutor_availability
    
def populate_subjects():
        subjects = [    # 20 subjects
            'Ruby_on_rails', 'Python', 'Javascript', 'C_plus_plus', 'C_sharp', 'React', 
            'Angular', 'Vue_js', 'Node_js', 'Express_js', 'Django', 'Flask', 
            'Spring', 'Hibernate', 'Jpa', 'Sql', 'Mongodb', 'Postgresql', 
            'Mysql', 'Git'
        ]
        for subject in subjects:
            Subjects.objects.get_or_create(subject_name=subject)
        print("Subjects populated.")



def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()

def create_email(first_name, last_name):
    return first_name + '.' + last_name + '@example.org'