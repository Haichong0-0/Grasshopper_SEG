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
    lessons = Lesson.objects.filter(tutor=request.user, invoice_no__isnull=False).select_related('invoice_no')
    total_students = invoices.values('student').distinct().count()
    total_balance = 0
    for lesson in lessons:
        if lesson.invoice_no:
            lesson.total_cost = lesson.invoice_no.price_per_class * lesson.invoice_no.no_of_classes
            total_balance += lesson.total_cost

    context = {
        'invoices': invoices,
        'total_students': total_students,
        'lessons': lessons,
        'total_balance':total_balance
    }

    return render(request, 'tutor/tutor_payment.html', context)



@login_required
@user_type_required('tutor')
def tutor_profile(request):
    return render(request, 'tutor/tutor_profile.html')



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


