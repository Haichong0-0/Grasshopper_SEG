from django.shortcuts import render, redirect
from tutorials.forms import LessonForm
from tutorials.models import Lesson, Invoice, Student
from django.contrib.auth.decorators import login_required 

def student_dashboard(request):

    context = {
        'user': 'Student!',
    }

    return render(request, 'student_dashboard_templates/student_dashboard.html', context)

def lesson_create_view(request):
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
                form.add_error('subject', 'You already have requsted a lesson for this subject.')
                return render(request, 'student_dashboard_templates/lesson_form.html', {'form': form})
            
            lesson.save()
            return redirect('student_schedule')
    else:
        form = LessonForm()
    return render(request, 'student_dashboard_templates/lesson_form.html', {'form': form})

def student_calenadr(request):
    pass


def student_invoices(request):

    invoices = Invoice.objects.all()

    context = {
        'invoices': invoices,
    }
    return render(request, 'student_dashboard_templates/student_invoices.html', context)


@login_required
def student_schedule(request):
    if request.user.is_authenticated and hasattr(request.user, 'student'):
        confirmed_lessons = Lesson.objects.filter(student=request.user, status='Confirmed').order_by('start_date','start_time')
        pending_lessons = Lesson.objects.filter(student=request.user, status='Pending').order_by('start_date','start_time')
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