from django.shortcuts import render, redirect
from tutorials.forms import LessonForm, MessageForm
from tutorials.models import Lesson, Invoice, Student
from django.contrib.auth.decorators import login_required 
from datetime import datetime, timedelta
from django.db.models import Q
from tutorials.models import Tutor, Subjects
from tutorials.decorators import user_type_required

    # vincent: TODO: add Docstrings for all classes and methods 
    # vincent: TODO: Docstrings on multiple lines for better readibilty
    # vincent: TODO: remove spacings within functions

@login_required
@user_type_required('student')
def student_dashboard(request):

    context = {
        'user': 'Student!',
    }

    return render(request, 'student/student_dashboard_in.html', context)

@login_required
@user_type_required('student')
def lesson_create_view(request):
    term_warning = None
    submit = 'Submit Lesson Request'
    button_class = 'btn-primary'
    hours = [str(hour) for hour in range(9, 18)]
    if request.method == 'POST':
        form = LessonForm(request.POST)
        
        if form.is_valid():
            lesson = form.save(commit=False)
        
            student = request.user.student 
            
            lesson.student = student
            
            # check if there is a lesson conflict 
            lesson_start_time = datetime.combine(datetime.today(), lesson.start_time)
            lesson_end_time = lesson_start_time + timedelta(minutes=int(lesson.duration))

            student_lessons = Lesson.objects.filter(student=student, day_of_week=lesson.day_of_week, term= lesson.term)
            for existing_lesson in student_lessons:
                existing_start_time = datetime.combine(datetime.today(), existing_lesson.start_time)
                existing_end_time = existing_start_time + timedelta(minutes=int(existing_lesson.duration))
                
                if lesson_start_time < existing_end_time and lesson_end_time > existing_start_time:
                    form.add_error('start_time', 'This lesson conflicts with another lesson in your schedule.')
                    return render(request, 'student/lesson_form.html', {
                        'form': form,
                        'term_warning': term_warning,
                        'submit': submit,
                        'button_class': button_class,
                        'hours': hours,
                    })

            # handle late lesson requests (after two weeks before the start of term)
            term_dates = {
                'September-Christmas': datetime(2024, 9, 2),
                'January-Easter': datetime(2025, 1, 6),
                'May-July': datetime(2025, 4, 21),
            }

            if 'submit_anyway' in request.POST:
                lesson.status = 'Late'
                lesson.save()
                return redirect('student_schedule')
                

            selected_term = lesson.term 

            if selected_term in term_dates:
                term_start = term_dates[selected_term]
                two_weeks_before_start = term_start - timedelta(weeks=2)
                current_date = datetime.now()

                if current_date > two_weeks_before_start:
                    term_warning = (
                        f"LATE REQUEST: Lesson requests must be submitted at least 2 weeks before the start of the {selected_term} term, "
                        f"which starts on {term_start.strftime('%Y-%m-%d')}. However, we may still be able to accommodate your request "
                        "depending on tutor availability."
                    )
                    submit = 'Submit Anyway'
                    button_class = 'btn-danger'

                    return render(request, 'student/lesson_form.html', {
                        'form': form, 
                        'term_warning': term_warning,
                        'submit': submit,
                        'button_class': button_class,
                        'hours': hours, 
                    })
        
            lesson.save()
            return redirect('student_schedule')

    else:
        form = LessonForm() 

    return render(request, 'student/lesson_form.html', {
        'form': form, 
        'term_warning': term_warning, 
        'submit': submit, 
        'button_class': button_class, 
        'hours': hours, 
    })

@login_required
@user_type_required('student')
def student_invoices(request):
    student = request.user
    invoices = Invoice.objects.filter(student=student).order_by('orderNo')

    context = {
        'invoices': invoices,
    }
    return render(request, 'student/student_invoices.html', context)

@login_required
@user_type_required('student')
def student_welcome(request):
    return render(request, 'student/student_welcome.html')


@login_required
@user_type_required('student')
def student_schedule(request):
    confirmed_lessons = Lesson.objects.filter(student=request.user, status='Confirmed').order_by('start_time')
    pending_lessons = Lesson.objects.filter(
            Q(student=request.user) & (Q(status='Pending') | Q(status='Late'))
        ).order_by('start_time')
    rejected_lessons = Lesson.objects.filter(student=request.user, status='Rejected').order_by('start_time')

    return render(request, 'student/student_schedule.html', {
        'confirmed_lessons': confirmed_lessons,
        'pending_lessons': pending_lessons,
        'rejected_lessons': rejected_lessons,
    })



  
@login_required
@user_type_required('student')
def leave_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.student = request.user.student
            message.save()
            return redirect('student_dashboard')
        else:
            return render(request, 'student/leave_message.html', {'form': form})
    else:
        form = MessageForm()
        return render(request, 'student/leave_message.html', {'form': form})

@login_required
@user_type_required('student')
def student_profile(request):
    return render(request, 'student/student_profile.html')
    
'''
@login_required
def sort_lessons(request):
    sort_by = request.GET.get('sort', 'date_asc')  # default 'date_asc' jic
    if sort_by == 'date_asc':
        lessons = Lesson.objects.all().order_by('start_time')  # ascend
    elif sort_by == 'date_desc':
        lessons = Lesson.objects.all().order_by('-start_time')  # descend
    elif sort_by == 'subject_asc':
        lessons = Lesson.objects.all().order_by('subject')  
    elif sort_by == 'subject_desc':
        lessons = Lesson.objects.all().order_by('-subject')  
    elif sort_by == 'reset': 
        lessons = Lesson.objects.all()  # maybe redundant
    else:
        lessons = Lesson.objects.all()  # no sorting
    
    return render(request, '.html', {'lessons': lessons})
    


@login_required
def sort_invoices(request):
    sort_by = request.GET.get('sort', 'date_asc')  # default 'date_asc' jic
    if sort_by == 'date_asc':
        invoice = Lesson.objects.all().order_by('start_time')  # ascend
    elif sort_by == 'date_desc':
        invoice = Lesson.objects.all().order_by('-start_time')  # descend
    elif sort_by == 'price_asc':
        invoice = Invoice.objects.all().order_by('totalsum')   #?? maybe need to change to price_per_class 
    elif sort_by == 'price_desc':
        invoice = Invoice.objects.all().order_by('-totalsum') 
    elif sort_by == 'reset': 
        invoice = Invoice.objects.all()  # maybe redundant
    else:
        invoice = Invoice.objects.all()  # no sorting
    
    return render(request, '.html', {'invoices': invoice})
    
'''