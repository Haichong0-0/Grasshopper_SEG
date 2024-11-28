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
