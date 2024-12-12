from django.shortcuts import render, redirect
from tutorials.forms import LessonForm
from tutorials.models import Lesson, Invoice, Student
from django.contrib.auth.decorators import login_required 
from datetime import datetime, timedelta
from tutorials.decorators import user_type_required



@login_required
@user_type_required('tutor')
def tutor_schedule(request):  
    confirmed_lessons = Lesson.objects.filter(tutor=request.user, status='confirmed').order_by('start_time')
    pending_lessons = Lesson.objects.filter(tutor=request.user, status='pending').order_by('start_time')

    return render(request, 'tutor/tutor_schedule.html', {
        'confirmed_lessons': confirmed_lessons,
        'pending_lessons': pending_lessons
    })


@login_required
@user_type_required('tutor')
def tutor_payments(request):
    invoices = Invoice.objects.filter(tutor=request.user)  
    
    total_students = invoices.values('student').distinct().count()
    total_balance_due = sum(invoice.total_sum for invoice in invoices)

    context = {
        'invoices': invoices,
        'total_students': total_students,
        'total_balance_due': total_balance_due,
    }

    return render(request, 'tutor/tutor_payment.html', context)



@login_required
@user_type_required('tutor')
def tutor_profile(request):
    return render(request, 'tutor/tutor_profile.html')


@login_required
def tutor_sort_lessons(request):
    sort_by = request.GET.get('sort', 'subject_asc') 
    
    pending_lessons = Lesson.objects.filter(status='Pending')
    confirmed_lessons = Lesson.objects.filter(status='Confirmed')  
    

    if sort_by == 'date_asc':
        pending_lessons = pending_lessons.order_by('start_time')
        confirmed_lessons = confirmed_lessons.order_by('start_time')
    elif sort_by == 'date_desc':
        pending_lessons = pending_lessons.order_by('-start_time')
        confirmed_lessons = confirmed_lessons.order_by('-start_time')
    elif sort_by == 'subject_asc':
        pending_lessons = pending_lessons.order_by('subject')
        confirmed_lessons = confirmed_lessons.order_by('subject')
    elif sort_by == 'subject_desc':
        pending_lessons = pending_lessons.order_by('-subject')
        confirmed_lessons = confirmed_lessons.order_by('-subject')
    else:
     
        pending_lessons = Lesson.objects.filter(status='Pending')
        confirmed_lessons = Lesson.objects.filter(status='Confirmed')

    return render(request, 'tutor/tutor_schedule.html', {
        'pending_lessons': pending_lessons,
        'confirmed_lessons': confirmed_lessons,
    })





@login_required
def tutor_sort_invoices(request):
    sort_by = request.GET.get('sort', 'price_asc')  
    
    if sort_by == 'price_asc':
        invoices = Invoice.objects.all().order_by('total_sum')  
    elif sort_by == 'price_desc':
        invoices = Invoice.objects.all().order_by('-total_sum')  
    elif sort_by == 'reset': 
        invoices = Invoice.objects.all()  
    else:
        invoices = Invoice.objects.all()  


    return render(request, 'tutor/tutor_payment.html', {'invoices': invoices})



