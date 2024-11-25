from django.shortcuts import render, redirect
from tutorials.forms import LessonForm
from tutorials.models import Lesson, Invoice

def student_dashboard(request):

    context = {
        'user': 'Student!',
    }

    return render(request, 'student_dashboard_templates/student_dashboard.html', context)

def lesson_create_view(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save() 
            #return redirect('lesson_list')
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

def student_schedule(request):
    if request.user.is_authenticated and hasattr(request.user, 'student'):
        lessons = Lesson.objects.filter(student=request.user.student).order_by('start_date','start_time')
    else:
        lessons = []

    context = {
        'lessons': lessons,
    }
    return render(request, 'student_dashboard_templates/student_schedule.html', context)