from django.shortcuts import render, redirect
from tutorials.forms import LessonForm
from tutorials.models import Lesson, Invoice, Student
from django.contrib.auth.decorators import login_required 
from datetime import datetime, timedelta
from django.db.models import Q


@login_required
def student_dashboard(request):

    context = {
        'user': 'Student!',
    }

    return render(request, 'student_dashboard_templates/student_dashboard_in.html', context)

@login_required
def lesson_create_view(request):
    term_warning = None 
    submit = 'Submit Lesson Request'
    button_class = 'btn-primary'
    if request.method == 'POST':
        form = LessonForm(request.POST)
        
        if form.is_valid():
            lesson = form.save(commit=False)
        
            try:
                student = request.user.student 
            except Student.DoesNotExist:
                return redirect('some_error_page')
            
            lesson.student = student

            if Lesson.objects.filter(student=student, subject=lesson.subject).exists():
                form.add_error('subject', 'You already have requested a lesson for this subject.')
                return render(request, 'student_dashboard_templates/lesson_form.html', {'form': form, 'term_warning': term_warning
                                                                                        ,'submit' : submit,'button_class': button_class})

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

                    return render(request, 'student_dashboard_templates/lesson_form.html', {
                        'form': form,
                        'term_warning': term_warning,
                        'submit' : submit,
                        'button_class': button_class
                    })
        
            lesson.save()
            return redirect('student_schedule')

    else:
        form = LessonForm() 
    
    return render(request, 'student_dashboard_templates/lesson_form.html', {'form': form, 'term_warning': term_warning, 'submit': submit, 'button_class': button_class})

@login_required
def student_invoices(request):

    invoices = Invoice.objects.all()

    context = {
        'invoices': invoices,
    }
    return render(request, 'student_dashboard_templates/student_invoices.html', context)

@login_required
def student_welcome(request):
    return render(request, 'student_dashboard_templates/student_welcome.html')


@login_required
def student_schedule(request):
    if request.user.is_authenticated and hasattr(request.user, 'student'):
        confirmed_lessons = Lesson.objects.filter(student=request.user, status='Confirmed').order_by('start_date','start_time')
        pending_lessons = Lesson.objects.filter(
            Q(student=request.user) & (Q(status='Pending') | Q(status='Late'))
        ).order_by('start_date', 'start_time')
        rejected_lessons = Lesson.objects.filter(student=request.user, status='Rejected').order_by('start_date','start_time')
    else:
        confirmed_lessons = []
        pending_lessons = []
        rejected_lessons = []

    return render(request, 'student_dashboard_templates/student_schedule.html', {
        'confirmed_lessons': confirmed_lessons,
        'pending_lessons': pending_lessons,
        'rejected_lessons': rejected_lessons,
    })