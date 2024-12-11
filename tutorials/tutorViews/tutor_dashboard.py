from django.shortcuts import render, redirect
from tutorials.forms import LessonForm
from tutorials.models import Lesson, Invoice, Student
from django.contrib.auth.decorators import login_required 
from datetime import datetime
from tutorials.decorators import user_type_required



@login_required
@user_type_required('tutor')
def tutor_schedule(request):
    confirmed_lessons = Lesson.objects.filter(
        tutor=request.user, 
        status='Confirmed'
    ).order_by('start_date', 'start_time')

    return render(request, 'tutor/tutor_schedule.html', {
        'confirmed_lessons': confirmed_lessons,
        'pending_lessons': pending_lessons,
        'rejected_lessons': rejected_lessons,
    })


@login_required
@user_type_required('tutor')
def tutor_payments(request):
    invoices = Invoice.objects.filter(tutor=request.user)  # Filter invoices for the tutor
    
    total_students = invoices.values('student').distinct().count()
    total_balance_due = sum(invoice.sum for invoice in invoices)
   # next_payment_due = invoices.order_by('due_date').first()  # Adjusted for clarity

    context = {
        'invoices': invoices,
        'total_students': total_students,
        'total_balance_due': total_balance_due,
        #'next_payment_due': next_payment_due.student if next_payment_due else None,
    }

    return render(request, 'tutor/tutor_payment.html', context)


@login_required
@user_type_required('tutor')
def tutor_lessons(request):
    current_date = datetime.now()
    start_of_week = current_date - timedelta(days=current_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    upcoming_lessons = Lesson.objects.filter(
        tutor=request.user, 
        start_date__range=[start_of_week, end_of_week]
    )

    context = {
        'upcoming_lessons_count': upcoming_lessons.count(),
    }

    return render(request, 'tutor/lessons.html', context)


@login_required
@user_type_required('tutor')
def tutor_profile(request):
    return render(request, 'tutor/tutor_profile.html')


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


