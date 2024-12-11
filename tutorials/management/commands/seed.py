from django.core.management.base import BaseCommand, CommandError
from tutorials.models import *
import pytz
from faker import Faker
from random import choice
import random
from tutorials.models import Subjects, Tutor # vincent: attempt to resolve available tutors not showing on admin lesson request page

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
    {'username': '@tutor', 'email': 'tutor@example.org', 'first_name': 'Tutor', 'last_name': 'Tutor'},
    {'username': '@jeroenkeppens', 'email': 'jeroen.keppens@example.org', 'first_name': 'Jeroen', 'last_name': 'Keppens'},
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
    {'user':'@tutor','subject':'ruby_on_rails','proficiency':'Intermediate'},
]

subject_names = [
    'Python', 'Django', 'React', 'JavaScript', 'SQL', 
    'C++', 'C#', 'Node.js', 'Flask', 'Spring'
]


student_fixtures = [
    {'username': '@student', 'email': 'student@example.org', 'first_name': 'Student', 'last_name': 'Student'},
]


lesson_fixtures = [
    {'student':'@student',
     'tutor':'@tutor',
     'subject':'ruby_on_rails',
     'frequency':'weekly',
     'terms':'September-Christmas',
     'duration':60,
    'day_of_week':'monday',
    'start_time':'10:00',
    'status':'confirmed',
    'invoice': 0,
     },
     {'student':'@student',
      'tutor':'@tutor',
      'subject':'python',
      'frequency':'fortnightly',
      'terms':'January-Easter',
      'duration':70,
      'day_of_week':'tuesday',
      'start_time':'15:00',
      'status':'pending',
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
    DEFAULT_PASSWORD = 'Password123!!'
    help = 'Seeds the database with sample data'

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        #self.create_users()
        # self.create_subjects()    
        populate_subjects()
        self.create_tutors()
        self.generate_tutor_availability()      # initially all tutors are free
        self.create_admins()
        self.create_students()
        self.generate_lesson_fixtures()
        print("Subjects end seed", Subjects.objects.get(subject_name="Javascript").tutor_list)
        
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

    # vincent: attempt to resolve available tutors not showing on admin lesson request page
    def create_subjects(self):
        subject_count = Subjects.objects.count()
        generated_subjects = 0

        print("subject count.")
        while subject_count < self.SUBJECT_COUNT:
            # print(f"Seeding Subject {subject_count + 1}/{self.SUBJECT_COUNT}", end='\r')

            generated_subjects = random.randint(0, len(subject_names)-1)
            subject_name = subject_names[generated_subjects]  
            # print("subject name: ", subject_name)
            
            self.try_create_subject({"subject_name": subject_name})
        
            subject_count = Subjects.objects.count()
        
        print("Subjects seeding complete.      ")


    def create_tutors(self):
        # populate_subjects()

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
        tutor.set_password(Command.DEFAULT_PASSWORD)  # This hashes the password
        tutor.save()

        tutor.subjects.add(*selected_subjects)
        print("tutor - 999: ", tutor)
        for subjects in selected_subjects:
            subjects.tutor_list.append(tutor.username)
            print("subjects.subject_name: ", subjects.subject_name)
            print("subjects.tutor_list.add(tutor): ", subjects.tutor_list)
            subjects.save()
        # print(f"Tutor {tutor.username} created with subjects: {', '.join([s.name for s in selected_subjects])}")
        print(f"Tutor {tutor.username} created with subjects: {', '.join([s.subject_name for s in selected_subjects])}")


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
            # user=data.get('user', None),  
        )
        subject.save()
        return subject

    def generate_lesson_fixtures(self):
        for data in lesson_fixtures:
            try:
                student = Student.objects.get(username=data['student'])  # Get Student instance
                tutor = Tutor.objects.get(username=data['tutor'])  # Get Tutor instance
                subject = Subjects.objects.get(subject_name=data['subject'])  # Get Subject instance
                
                invoice = self.try_create_invoice(invoice_fixtures[data['invoice']])
                
                Lesson.objects.create(
                    student=student,
                    tutor=tutor,
                    subject=subject,
                    frequency=data['frequency'],
                    term=data['terms'],
                    duration=data['duration'],
                    day_of_week=data['day_of_week'],
                    start_time=data['start_time'],
                    status=data['status'],
                    invoiceNo=invoice,
                )
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
        print(f"Created full availability for Tutor: {tutor.username}")

    
    def try_create_invoice(self, data):
        try:
            return self.create_invoice(data)
        except Exception as e:
            print(f"Error creating invoice: {e}")
            return None
    
    def create_invoice(self, data):
        
        invoice = Invoice.objects.create(
            no_of_classes=data['no_of_classes'],
            price_per_class=data['price_per_class'],
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
            invoiceNo=invoice,
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


