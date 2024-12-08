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

    return render(request, 'tutor_dashboard/tutor_schedule.html', {
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
    next_payment_due = invoices.order_by('due_date').first()  # Adjusted for clarity

    context = {
        'invoices': invoices,
        'total_students': total_students,
        'total_balance_due': total_balance_due,
        'next_payment_due': next_payment_due.student if next_payment_due else None,
    }

    return render(request, 'tutor_dashboard/tutor_payment.html', context)


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

    return render(request, 'tutor_dashboard/lessons.html', context)


@login_required
def tutor_profile(request):
    context = {

    }
    return render(request, 'tutor_dashboard/tutor_profile.html', context)