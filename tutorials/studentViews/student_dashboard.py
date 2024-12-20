from django.shortcuts import render, redirect
from tutorials.forms import LessonForm, MessageForm
from tutorials.models import Lesson, Invoice, Student
from django.contrib.auth.decorators import login_required 
from datetime import datetime, timedelta
from django.db.models import Q
from tutorials.models import Tutor, Subjects
from tutorials.decorators import user_type_required
from django.shortcuts import get_object_or_404


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
    lessons = Lesson.objects.filter(student=student, invoice_no__isnull=False).select_related('invoice_no')
    for lesson in lessons:
        if lesson.invoice_no:
            lesson.total_cost = lesson.invoice_no.price_per_class * lesson.invoice_no.no_of_classes
    context = {
        'invoices': invoices,
        'lessons': lessons
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


@login_required
@user_type_required('student')
def make_payment(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        start_time = request.POST.get('start_time')
        day_of_week = request.POST.get('day_of_week')
        if subject and start_time and day_of_week:
            lesson = get_object_or_404(Lesson, student=request.user, subject=subject, day_of_week=day_of_week, status__in=['Pending', 'Late'], payment_status='Unpaid')
            lesson.payment_status = 'Paid'
            lesson.save()
            return redirect('student_schedule')
    unpaid_pending_lessons = Lesson.objects.filter(student=request.user, status__in=['Pending', 'Late'], payment_status='Unpaid')
    return render(request, 'student/make_payment.html', {
        'unpaid_pending_lessons': unpaid_pending_lessons,
    })


