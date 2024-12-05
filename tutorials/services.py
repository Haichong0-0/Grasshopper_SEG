from .models import *

def get_user_type(user):
    """Return the type of user."""
    
    if hasattr(user, 'admin'):
        return 'admin'
    elif hasattr(user, 'tutor'):
        return 'tutor'
    elif hasattr(user, 'student'):
        return 'student'
    else:
        return 'unknown'
    
def get_tutor_Bytime(day_of_week,time):
    """Return a list of tutors available at the current time."""
    
    tutors = Tutor.objects.filter(
        day=day_of_week,
        start_time__lte=time,
        end_time__gte=time
    )
    return tutors

def book_lesson(student, tutor,subject,frequency,term,day_of_week,start_time,duration,price_per_lesson):
    """Book a lesson."""
    

    FREQUENCY_CHOICES = [
        ('weekly', 1),
        ('fortnightly', 2),
    ]

    no_of_lessons = 12/ FREQUENCY_CHOICES [frequency][1]

    invoice = Invoice.objects.create(
        no_of_lessons=no_of_lessons,
        price_per_lesson=price_per_lesson
    )
    invoice.calc_sum()

    Lesson.objects.create(
        student=student,
        tutor=tutor,
        day_of_week=day_of_week,
        start_time=start_time,
        duration=duration,
        frequency=frequency,
        term=term,
        subject=subject,
        status='pending',
        invoiceNo=invoice
    )

    remove_tutor_availability(tutor, day_of_week, start_time, start_time+duration)
    return invoice

def remove_tutor_availability(tutor, day, start_time, end_time):
    
    tutor_availability = TutorAvailability.objects.get(
        tutor=tutor,
        day=day,
        start_time__lte=start_time,
        end_time__gte=end_time
    )
    if (tutor_availability.start_time == start_time) and (tutor_availability.end_time == end_time):
        tutor_availability.delete()
    elif tutor_availability.start_time == start_time:
        tutor_availability.start_time = end_time
    elif tutor_availability.end_time == end_time:
        tutor_availability.end_time = start_time
    else:
        tutor_availability.endtime = end_time

def tutor_subject(tutor):
    """Return a list of subjects taught by a tutor."""

    tutorobject = Tutor.objects.get(tutor=tutor)
    
    return tutor.subject_set.all()


def get_all_tutor(time, day,subject):
    """Return a list of tutors available at the current time."""
    available_tutors = set()

    availables = TutorAvailability.objects.filter(
        day=day,
        starttime__lte=time,
        endtime__gte=time
    )

    for available in availables:
        tutor = available.tutor

        if Subjects.objects.filter(user=tutor, subject=subject).exists():
            available_tutors.add(tutor.username)

    return list(available_tutors)

def add_tutor_availability(tutor, day, start_time, end_time):
    """Add availability for a tutor."""
    
    TutorAvailability.objects.create(
        tutor=tutor,
        day=day,
        start_time=start_time,
        end_time=end_time
    )

def get_tutor_shedule(tutor):
    return Lesson.objects.filter(tutor=tutor),TutorAvailability.objects.filter(tutor=tutor)

def get_student_shedule(student):
    return Lesson.objects.filter(student=student)

def check_student_availability(student, day, start_time):
    """Check if a student is available at the given time."""
    
    lessons = Lesson.objects.filter(
        student=student,
        day=day,
        start_time__lte=start_time,
    )
    return not lessons.exists()