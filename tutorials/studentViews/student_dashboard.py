from django.shortcuts import render, redirect
from tutorials.forms import LessonForm
from tutorials.models import Lesson

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