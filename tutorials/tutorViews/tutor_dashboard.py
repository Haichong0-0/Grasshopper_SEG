from django.shortcuts import render, redirect
from tutorials.forms import LessonForm
from tutorials.models import Lesson, Invoice, Student
from django.contrib.auth.decorators import login_required 
from datetime import datetime




@login_required
def tutor_schedule(request):
    if request.user.is_authenticated and hasattr(request.user, 'tutor'):
        confirmed_lessons = Lesson.objects.filter(tutor=request.user, status='Confirmed').order_by('start_date','start_time')
    else:
        confirmed_lessons = []
      
    return render(request, 'tutor_dashboard/tutor/schedule/tutor_schedule.html', {
        'confirmed_lessons': confirmed_lessons,
        'pending_lessons': pending_lessons,
        'rejected_lessons': rejected_lessons,
    })


@login_required
def tutor_payments(request):
    invoices = Invoice.objects.all()
    
    total_students = invoices.values('student').distinct().count()
    total_balance_due = sum(invoice.sum for invoice in invoices)
    next_payment_due = invoices.order_by('sum').first().student if invoices else None  
    
    context = {
        'invoices': invoices,
        'total_students': total_students,
        'total_balance_due': total_balance_due,
        'next_payment_due': next_payment_due,
    }
    
    return render(request, 'tutor_dashboard/tutor_payment.html', context)



@login_required
def tutor_lessons(request):
    # get the current week dates (
    current_date = datetime.now()
    start_of_week = current_date - timedelta(days=current_date.weekday()) 
    end_of_week = start_of_week + timedelta(days=6)  
    
    # filter lessons that are happening this week
    upcoming_lessons = Lesson.objects.filter(
        tutor=request.user.tutor,
        start_date__gte=start_of_week,
        start_date__lte=end_of_week
    )
    
    context = {
        'upcoming_lessons_count': upcoming_lessons.count(),
    }

    return render(request, 'tutor_dashboard/tutor/lessons.html', context)


@login_required
def tutor_profile(request):
    context = {

    }
    return render(request, 'tutor_dashboard/tutor_profile.html', context)


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
    
    return render(request, 'your_template.html', {'lessons': lessons})


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
    
    return render(request, 'your_invoice_template.html', {'invoices': invoice})


    
