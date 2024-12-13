from django.shortcuts import render, redirect
from tutorials.forms import LessonForm, UpdateSubjectsForm
from tutorials.models import Lesson, Invoice, Student, Subjects, Tutor
from django.contrib.auth.decorators import login_required 
from datetime import datetime, timedelta
from tutorials.decorators import user_type_required



@login_required
@user_type_required('tutor')
def tutor_schedule(request):  
    confirmed_lessons = Lesson.objects.filter(tutor=request.user, status='Confirmed').order_by('start_time')

    return render(request, 'tutor/tutor_schedule.html', {
        'confirmed_lessons': confirmed_lessons,
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


def update_subjects(request):
    tutor = request.user.tutor  
    if request.method == 'POST':
        form = UpdateSubjectsForm(request.POST)
        if form.is_valid():
            selected_subjects = form.cleaned_data['subjects']
            subjects_to_add = []
            for subject_code in selected_subjects:
                subject_name = dict(Tutor.SUBJECTS).get(subject_code)
                if subject_name:
                    subject, created = Subjects.objects.get_or_create(subject_name=subject_name)
                    subjects_to_add.append(subject)
            tutor.subjects.set(subjects_to_add)
            tutor.save()
            return redirect('tutor_profile')
        else:
            print('Form is not valid')
    else:
        form = UpdateSubjectsForm()

    return render(request, 'tutor/update_subjects.html', {'form': form, 'tutor': tutor})


