from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from tutorials.forms import LogInForm, PasswordForm, UserForm, SignUpForm, MessageForm
from tutorials.helpers import login_prohibited
from tutorials.models import User, Lesson, Tutor, Student, Invoice, TutorAvailability, Subjects
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serialiser import LessonSerializer
from datetime import datetime, date, timedelta
from django.db.models import Q
from django.shortcuts import render, get_object_or_404


#############################################################
'''from .models import Admin, Tutor, Student, Lesson, Invoice
from .forms import AdminForm, TutorForm, StudentForm, LessonForm, InvoiceForm'''

from django.views.generic import CreateView, ListView, DeleteView




@login_required
def admin_dashboard(request):
    """Display the admin's dashboard."""

    current_user = request.user
    if (current_user.type_of_user == 'admin'):

        print("current_user(admin_dashboard): ", current_user.type_of_user)
        return render(request, 'admin_dashboard.html', {'user': current_user})
    else:
        return render(request, 'access_denied.html', {'user': current_user})

@login_required
def tutor_dashboard(request):
    """Display the tutor's dashboard."""

    current_user = request.user
    if (current_user.type_of_user == 'tutor'):
        print("current_user(tutor_dashboard): ", current_user)
        return render(request, 'tutor_dashboard/tutor_dashboard.html', {'user': current_user})
    else:
        return render(request, 'access_denied.html', {'user': current_user})

@login_required
def student_dashboard(request):
    """Display the student's dashboard."""

    current_user = request.user
    if (current_user.type_of_user == 'student'):
        print("current_user(student_dashboard): ", current_user)
        return render(request, 'student_dashboard.html', {'user': current_user})
    else:
        return render(request, 'access_denied.html', {'user': current_user})


@login_prohibited
def home(request):
    """Display the application's start/home screen."""
    print(request.user.is_authenticated) # for testing purposes
    return render(request, 'home.html')


class LoginProhibitedMixin:
    """Mixin that redirects when a user is logged in."""

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        print("after handle_already_logged_in: ", url)
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url


class LogInView(LoginProhibitedMixin, View):
    """Display login screen and handle user login."""

    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get(self, request):
        """Display log in template."""

        self.next = request.GET.get('next') or ''
        print("get(): ", self.next)
        return self.render()

    def post(self, request):
        """Handle log in attempt."""

        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user(request)
        print("after post(): ", user)

        if user is not None:
            try:
                login(request, user)
            
            except Exception as e:
                print("error occured at login: ",e)

            if user.type_of_user=="student":  
                print(self.next)
                return redirect(reverse('student_dashboard'))
            elif user.type_of_user=="tutor":  
                return redirect(reverse('tutor_dashboard'))
            elif user.type_of_user=="admin":  
                return redirect(reverse('admin_dashboard'))
        
        else: 
            print("login_view, user is None: ", user)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """Render log in template with blank log in form."""

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})


def log_out(request):
    """Log out the current user"""

    logout(request)
    return redirect('home')


class PasswordView(LoginRequiredMixin, FormView):
    """Display password change screen and handle password change requests."""

    template_name = 'password.html'
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the password change form."""

        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form by saving the new password."""

        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user after successful password change."""

        messages.add_message(self.request, messages.SUCCESS, "Password updated!")
        return reverse('dashboard')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Display user profile editing screen, and handle profile modifications."""

    model = UserForm
    template_name = "profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(self.request, messages.SUCCESS, "Profile updated!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)



class UserListView(ListView): #need to make test
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return User.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(email__icontains=query)
            )
        return User.objects.all()


def is_admin(user):
    return user.is_staff 

@login_required
@user_passes_test(is_admin)
def admin_lessons(request):
    """lessons page for admins"""

    context = {}

    return render(request, 'admin_lessons.html', context)

"""@login_required
def tutor_dashboard(request):
    display tutor dashboard if user is a tutor
    
    context = {
        'full_name': request.user.full_name(),
        'gravatar': request.user.gravatar(),
    }
    
    return render(request, 'tutor_dashboard.html', context)
"""

#@login_required
def tutor_lessons(request):
    """lessons page for tutors"""

    context = {

    }

    return render(request, 'tutor_lessons.html', context)

class SignUpView(LoginProhibitedMixin, FormView): 
    """Display the sign-up screen and handle sign-ups."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request  # Pass the request object

        print('coming from get_form_kwargs: ', kwargs)  # Deyu: for testing
        return kwargs

    def get_context_data(self, **kwargs):
        # Add a custom message based on the user_type
        context = super().get_context_data(**kwargs)
        variation = self.request.GET.get('variation')

        if variation == 'student':
            context['message'] = "Student Sign-Up Form"
        elif variation == 'tutor':
            context['message'] = "Tutor Sign-Up Form"

        context['user_type'] = variation
        return context

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Log form errors for debugging."""
        print("Form errors:", form.errors)  # Log errors to console
        return super().form_invalid(form) 

    def get_success_url(self):
        """Redirect based on user type."""

        user = self.request.user
        if user.type_of_user=="admin":   # Admin user
            return reverse('admin_dashboard')
        elif user.type_of_user=="tutor":  
            return reverse('tutor_dashboard')
        elif user.type_of_user=="student":  
            print('after get_success_url')
            return reverse('student_dashboard')
        else:
            print('after get_success_url, else statement')
            return reverse('home')

@login_required
@user_passes_test(is_admin)
def admin_welcome(request):
    """welcome page for admins"""

    context = {

    }

    return render(request, 'admin_welcome.html', context)


# @login_required
def tutor_welcome(request):
    """welcome page for tutors"""

    context = {

    }

    return render(request, 'tutor_dashboard/tutor_welcome.html', context)


def leave_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.student = request.user.student
            message.save()
            return redirect('student_dashboard')

    else:
        form = MessageForm()
        return render(request, 'student_dashboard_templates/leave_message.html', {'form': form})






def get_tutor(time, day, subject):


    print(time, day, subject.capitalize())
    available_tutors = set()

    print("tutor_list 999", Subjects.objects.get(subject_name=subject.capitalize()).tutor_list)
    tutor_list = Subjects.objects.get(subject_name=subject.capitalize()).tutor_list

    for tutor in tutor_list:
        available_tutors.add(Tutor.objects.get(username=tutor))
    
    return list(available_tutors)


def get_lesson_data():
    context = {}

    confirmed_lessons = Lesson.objects.filter(status='Confirmed').order_by('-start_time')
    pending_lessons = Lesson.objects.filter(Q(status='Pending') | Q(status='Late')).order_by('-start_time')
    rejected_lessons = Lesson.objects.filter(status='Rejected').order_by('-start_time')

    for lesson in pending_lessons:
        lesson.duration = lesson.duration // 60      # Convert duration to hours
        print("subject: ", lesson.start_time, lesson.day_of_week, lesson.subject,)
        lesson.available_tutors=get_tutor(time=lesson.start_time, day=lesson.day_of_week, subject=lesson.subject)
   
        lesson_start_time = datetime.combine(datetime.today(), lesson.start_time)
        lesson_end_time = lesson_start_time + timedelta(minutes=int(lesson.duration))

        filtered_tutors = []
        for tutor in lesson.available_tutors:
            try:
                un = tutor.username
                tutor = Tutor.objects.get(username=un)
                if not TutorAvailability.objects.filter(
                    tutor=tutor,
                    day=lesson.day_of_week,
                    starttime__lt=lesson_end_time.time(), 
                    endtime__gt=lesson_start_time.time()
                ).exists():
                    filtered_tutors.append(tutor)
            except Tutor.DoesNotExist:
                print(f"Tutor with username '{un}' does not exist.")

        lesson.available_tutors = filtered_tutors


    context["confirmed_lessons"] = confirmed_lessons
    context["pending_lessons"] = pending_lessons       
    context["rejected_lessons"] = rejected_lessons
    # context["available_tutors"] = TutorAvailability.objects.all()
    

    return context

@login_required
@user_passes_test(is_admin)
def admin_schedule(request):
    """schedule page for tutors"""


    if request.user.is_authenticated and hasattr(request.user, 'admin'):
        context = get_lesson_data()


    return render(request, 'admin_schedule.html', context)

@login_required
def tutor_schedule(request):
    """schedule page for tutors"""

    context = {

    }

    return render(request, 'tutor_schedule.html', context)

@login_required
@user_passes_test(is_admin)
def admin_payment(request):
    """payment page for admin"""

    context = {

    }

    invoice_detail = Invoice.objects.all().order_by('-orderNo')
    context["pending_lessons"] = invoice_detail 
    # context["available_tutors"] = Tutor.objects.all()

    return render(request, 'admin_payment.html', context)


@login_required
def tutor_payment(request):
    """payment page for tutors"""

    invoices = []  # Return an empty queryset if the user is not a tutor

    context = {}

    return render(request, 'tutor_payment.html', context)

@login_required
def student_payment(request):
    """payment page for admin"""

    if hasattr(request.user, 'student'):  # Ensure the user is a student
        invoices = Invoice.objects.filter(student=request.user.student).order_by('-orderNo')
    else:
        invoices = []  # Return an empty queryset if the user is not a student

    context = {
        'invoices': invoices,
    }

    return render(request, 'student_payment.html', context)

@login_required
@user_passes_test(is_admin)
def admin_messages(request):
    """payment page for admin"""

    context = {

    }

    return render(request, 'admin_payment.html', context)

# working, without the tutoravailability function
class ConfirmClassView(APIView):
    
    def post(self, request, lesson_id):
        request_data = request.data
        print('received the request with data', request.POST)       # testing
        
        serializer = LessonSerializer(data=request_data)
        if serializer.is_valid():
            print('valid data: success')
            lesson_obj = Lesson.objects.get(lesson_id=lesson_id)
            # price_per_class = Invoice.objects.price_per_class


            invoice = Invoice.objects.filter(orderNo=lesson_obj.invoiceNo).first() 
            if not invoice:
                return redirect("admin_schedule")

            price_per_class = invoice.price_per_class  
            print(f"Price per class: {price_per_class}")


            if(request.POST.get("tutor")):
                tutor = Tutor.objects.get(id=request.POST.get("tutor"))  # Fetch the Tutor object
                lesson_obj.tutor = tutor  # Assign the Tutor object

                lesson_obj.status = "Confirmed"
                lesson_obj.save()

            
            no_of_classes = lesson_obj.duration//60
            print("no_of_classes: ", type(no_of_classes), no_of_classes)
            

            total = no_of_classes * price_per_class

        try:
            Invoice.objects.create(                
                tutor=Tutor.objects.get(id=request.POST.get("tutor")),
                student=Student.objects.get(id=lesson_obj.student_id),
                topic=lesson_obj.subject,
                no_of_classes=no_of_classes,
                price_per_class=price_per_class,
                total_sum=total
            )
        except Exception as e:
            print(f"Error creating invoice: {e}")
            return redirect("admin_schedule")

        else:
            return redirect("admin_schedule")


class RejectClassView(APIView):
    
    def post(self, request, lesson_id):
        request_data = request.data
        print('RejectClassView', request.POST)       # testing
        
        serializer = LessonSerializer(data=request_data)
        if serializer.is_valid():
            print('RejectClassView valid data: success')
            lesson_obj = Lesson.objects.get(lesson_id=lesson_id)

            print("inside if-statement.")
            lesson_obj.status = "Rejected"
            lesson_obj.save()

            return redirect("admin_schedule")

        else:
            return redirect("admin_schedule")
    


@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'user_profile.html', {'user': user})