from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from tutorials.forms import LogInForm, PasswordForm, UserForm, SignUpForm, MessageForm
from tutorials.helpers import login_prohibited
from tutorials.models import User, Lesson, Tutor, Student, Invoice, TutorAvailability, Subjects, Message
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serialiser import LessonSerializer

from datetime import datetime, date, timedelta
from django.db.models import Q
from django.shortcuts import render, get_object_or_404


from tutorials.decorators import user_type_required


#############################################################
'''from .models import Admin, Tutor, Student, Lesson, Invoice
from .forms import AdminForm, TutorForm, StudentForm, LessonForm, InvoiceForm'''

from django.views.generic import CreateView, ListView, DeleteView




@login_required
def admin_dashboard(request):
    """  
    Display the admin's dashboard.
    """
    # vincent: Docstrings on 3 lines for better readibilty (remove these comments in final version)
    # vincent: TODO: change all Docstrings to multiple lines
    # vincent: TODO: remove spacings within functions

    current_user = request.user
    if (current_user.type_of_user == 'admin'):

        print("current_user(admin_dashboard): ", current_user.type_of_user)
        return render(request, 'admin/admin_dashboard.html', {'user': current_user})
    else:
        return render(request, 'access_denied.html', {'user': current_user})

# @login_required
# def tutor_dashboard(request):
#     """Display the tutor's dashboard."""

#     current_user = request.user
#     if (current_user.type_of_user == 'tutor'):
#         print("current_user(tutor_dashboard): ", current_user)
#         return render(request, 'tutor_dashboard/tutor_dashboard.html', {'user': current_user})
#     else:
#         return render(request, 'access_denied.html', {'user': current_user})

# @login_required
# def student_dashboard(request):
#     """Display the student's dashboard."""

#     current_user = request.user
#     if (current_user.type_of_user == 'student'):
#         print("current_user(student_dashboard): ", current_user)
#         return render(request, 'student_dashboard.html', {'user': current_user})
#     else:
#         return render(request, 'access_denied.html', {'user': current_user})
    
@login_required
@user_type_required('tutor')
def tutor_dashboard(request):
    """
    Display the tutor's dashboard.
    """

    current_user = request.user
    if (current_user.type_of_user == 'tutor'):
        print("current_user(tutor_dashboard): ", current_user)
        return render(request, 'tutor/tutor_dashboard.html', {'user': current_user})
    else:
        return render(request, 'access_denied.html', {'user': current_user})

@login_required
@user_type_required('student')
def student_dashboard(request):
    """
    Display the student's dashboard.
    """

    current_user = request.user
    if (current_user.type_of_user == 'student'):
        print("current_user(student_dashboard): ", current_user)
        return render(request, 'student/student_dashboard.html', {'user': current_user})
    else:
        return render(request, 'access_denied.html', {'user': current_user})


@login_prohibited
def home(request):
    """
    Display the application's start/home screen.
    """
    print(request.user.is_authenticated) # vincent: TODO: (remove this line in final version)for testing purposes
    return render(request, 'home.html')


class LoginProhibitedMixin:
    """
    Mixin that redirects when a user is logged in.
    """

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """
        Redirect when logged in, or dispatch as normal otherwise.
        """
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        print("after handle_already_logged_in: ", url)
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """
        Returns the url to redirect to when not logged in.
        """
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url


class LogInView(LoginProhibitedMixin, View):
    """
    Display login screen and handle user login.
    """

    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get(self, request):
        """
        Display log in template.
        """

        self.next = request.GET.get('next') or ''
        print("get(): ", self.next)
        return self.render()

    def post(self, request):
        """
        Handle log in attempt.
        """

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
        """
        Render log in template with blank log in form.
        """

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})


def log_out(request):
    """
    Log out the current user
    """

    logout(request)
    return redirect('home')


class PasswordView(LoginRequiredMixin, FormView):
    """
    Display password change screen and handle password change requests.
    """

    template_name = 'password.html'
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """
        Pass the current user to the password change form.
        """

        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """
        Handle valid form by saving the new password.
        """

        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirect the user after successful password change.
        """

        messages.add_message(self.request, messages.SUCCESS, "Password updated!")
        return reverse('dashboard')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Display user profile editing screen, and handle profile modifications.
    """

    model = UserForm
    template_name = "profile.html"
    form_class = UserForm

    def get_object(self):
        """
        Return the object (user) to be updated.
        """
        user = self.request.user
        return user

    def get_success_url(self):
        """
        Return redirect URL after successful update.
        """
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
    """
    lessons page for admins
    """

    context = {}

    return render(request, 'admin/admin_lessons.html', context)

"""@login_required
def tutor_dashboard(request):
    display tutor dashboard if user is a tutor
    
    context = {
        'full_name': request.user.full_name(),
        'gravatar': request.user.gravatar(),
    }
    
    return render(request, 'tutortutor_dashboard.html', context)
"""

#@login_required
def tutor_lessons(request):
    """
    lessons page for tutors
    """

    context = {}

    return render(request, 'tutor/tutor_lessons.html', context)

class SignUpView(LoginProhibitedMixin, FormView): 
    """
    Display the sign-up screen and handle sign-ups.
    """

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    
    def get_form_kwargs(self)->dict:       
        """
        get all sign_up_form data in dictionary
        """
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request  # Pass the request object
        print('coming from get_form_kwargs: ', kwargs)  # vincent: TODO: instead of logging, print instead. log instead
        return kwargs

    def get_context_data(self, **kwargs)->dict:
        """
        get context_data with sign_up_form
        """
        context = super().get_context_data(**kwargs)
        variation = self.request.GET.get('variation')
        # Add a custom message based on the user_type
        if variation == 'student':
            context['message'] = "Student Sign-Up Form"
        elif variation == 'tutor':
            context['message'] = "Tutor Sign-Up Form"
        context['user_type'] = variation
        return context

    def form_valid(self, form)-> HttpResponse:
        """
        Handle valid form submission.

        This method saves the form, logs in the user associated with 
        the form, and then calls the parent class's `form_valid` method.
        """
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)
    
    def form_invalid(self, form)-> HttpResponse:
        """
        Log form errors for debugging.
        """
        print("Form errors:", form.errors)  # Log errors to console
        return super().form_invalid(form) 

    def get_success_url(self)-> HttpResponse:
        """                 # seperate this comment to 3 lines for readibility
        Redirect user to their respective dashboard after sign up based on user type.
        """
        user = self.request.user
        if user.type_of_user=="admin":   
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
def admin_welcome(request)-> HttpResponse:
    """
    welcome page for admins
    """
    return render(request, 'admin/admin_welcome.html', context = {})


@login_required
def tutor_welcome(request)-> HttpResponse:
    """
    welcome page for tutors
    """
    return render(request, 'tutor/tutor_welcome.html', context = {})

def leave_message(request)-> HttpResponse:      
    """
    student leaving messages for admins
    """
    if request.method == 'POST':
        # saving student message request 
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.student = request.user.student
            message.save()
            return redirect('student_dashboard')
    form = MessageForm()
    return render(request, 'student/leave_message.html', {'form': form})

def get_tutor(subject)->list:
    """
    return available list of tutors on the basis on subjects
    """
    available_tutors = set()
    # fetching tutor list from Subjects table, if subject matches 
    tutor_list = Subjects.objects.get(subject_name=subject.capitalize()).tutor_list
    for tutor in tutor_list:       
        # adding tutor objects to available_tutors list 
        available_tutors.add(Tutor.objects.get(username=tutor))
    return list(available_tutors)


def get_lesson_data()->dict:        # vincent TODO: complete refactoring (remove this comment in final version)
    """
    extracting all lesson datas with associated available tutors
    """
    context = {}

    # filtering lesson data on the basis of status, and sorting the data by 'start_time' in descending order
    confirmed_lessons = Lesson.objects.filter(status='Confirmed').order_by('-start_time')
    pending_lessons = Lesson.objects.filter(Q(status='Pending') | Q(status='Late')).order_by('-start_time')
    rejected_lessons = Lesson.objects.filter(status='Rejected').order_by('-start_time')

    for lesson in pending_lessons:
        lesson.duration = lesson.duration // 60      # Convert duration to hours
        # get available_tutor by calling get_tutor function
        lesson.available_tutors=get_tutor(subject=lesson.subject)
        # combining date with time to calculate lesson_start_time and lesson_end_time
        lesson_start_time = datetime.combine(datetime.today(), lesson.start_time)
        lesson_end_time = lesson_start_time + timedelta(minutes=int(lesson.duration))

        filtered_tutors = []
        for tutor in lesson.available_tutors:
            try:
                tutor_username = tutor.username
                tutor = Tutor.objects.get(username=tutor_username)
                # filtering available tutor by start_time, end_time and day
                if not TutorAvailability.objects.filter(
                    tutor=tutor,
                    day=lesson.day_of_week,
                    starttime__lt=lesson_end_time.time(), 
                    endtime__gt=lesson_start_time.time()
                ).exists():
                    filtered_tutors.append(tutor)
            except Exception as e:
                print("Exception occurred while filtering tutors: ", e)
        # updating Lesson object with available tutors
        lesson.available_tutors = filtered_tutors
    # updating context with lesson details
    context["confirmed_lessons"] = confirmed_lessons
    context["pending_lessons"] = pending_lessons       
    context["rejected_lessons"] = rejected_lessons
    return context

@login_required
@user_passes_test(is_admin)
def admin_schedule(request)-> HttpResponse:
    """
    schedule page for admin to manage lesson requests
    """
    if request.user.is_authenticated and hasattr(request.user, 'admin'):
        # getting lesson_data for admin to manage, with a list of available tutors
        context = get_lesson_data()
    return render(request, 'admin/admin_schedule.html', context)

@login_required
def tutor_schedule(request)-> HttpResponse:
    """
    schedule page for tutors
    """
    return render(request, 'tutor/tutor_schedule.html', context={})

@login_required
@user_passes_test(is_admin)
def admin_payment(request)-> HttpResponse:
    """
    payment page for admin
    """
    context = {}
    # getting all invoice objects, sorted by orderNo, in descending order
    invoice_detail = Invoice.objects.all().order_by('-orderNo')
    context["invoice_detail"] = invoice_detail 
    return render(request, 'admin/admin_payment.html', context)


@login_required
def tutor_payment(request)-> HttpResponse:
    """payment page for tutors"""

    invoices = []  # Return an empty queryset if the user is not a tutor

    context = {}

    return render(request, 'tutor/tutor_payment.html', context)

@login_required
def student_payment(request)-> HttpResponse:
    """
    payment page for admin
    """
    if hasattr(request.user, 'student'):  # Ensure the user is a student
        invoices = Invoice.objects.filter(student=request.user.student).order_by('-orderNo')
    else:
        invoices = []  # Return an empty queryset if the user is not a student
    context = {
        'invoices': invoices,
    }
    return render(request, 'student/student_payment.html', context)

@login_required
@user_passes_test(is_admin)
def admin_messages(request)-> HttpResponse:
    """
    payment page for admin
    """
    context = {}
    return render(request, 'admin/admin_messages.html', context)

# check the tutoravailability function
class ConfirmClassView(APIView):        # Vincent: complete 'refactoring'
    def post(self, request, lesson_id)-> HttpResponse:
        """
        accept button for admins to accept lesson requests from students
        """
        # get request data from POST request
        request_data = request.data
        # validate the incoming data
        serializer = LessonSerializer(data=request_data)
        if serializer.is_valid():
            # retreive the lesson object based on the lesson_id
            lesson_obj = Lesson.objects.get(lesson_id=lesson_id)
            # checks if a tutor ID is provided in the POST request
            if(request.POST.get("tutor")):
                # get the tutor object based on the provided tutor ID
                tutor = Tutor.objects.get(id=request.POST.get("tutor"))  # Fetch the Tutor object
                lesson_obj.tutor = tutor  # Assign the Tutor object
                lesson_obj.status = "Confirmed" # update its status
                # calculate the no_of_classes
                no_of_classes = lesson_obj.duration//60
                # calculate the total price of classes
                total_price = no_of_classes * 20
                # create an invoice for the lesson
                invoice = Invoice.objects.create(                
                    tutor=Tutor.objects.get(id=request.POST.get("tutor")),
                    student=Student.objects.get(id=lesson_obj.student_id),
                    topic=lesson_obj.subject,
                    no_of_classes=no_of_classes,
                    total_sum=total_price
                )
                lesson_obj.invoice_no = invoice
                lesson_obj.save()
                # create a tutor availability for the lesson (mark the tutor unavailable during lesson time)
                lesson_start_time = datetime.combine(datetime.today(), lesson_obj.start_time)
                lesson_end_time = lesson_start_time + timedelta(minutes=int(lesson_obj.duration))
                tutor_availability = TutorAvailability.objects.create(
                    tutor=lesson_obj.tutor,
                    day=lesson_obj.day_of_week,
                    starttime=lesson_start_time,
                    endtime = lesson_end_time
                )
                tutor_availability.save()
        return redirect("admin_schedule")


class RejectClassView(APIView):  # Vincent: complete 'refactoring'
    def post(self, request, lesson_id)-> HttpResponse:
        """
        reject button for admins to reject lesson requests from students
        """
        # get the data from the POST request
        request_data = request.data
        # validate the lesson object based on the lesson_id
        serializer = LessonSerializer(data=request_data)
        if serializer.is_valid():
            # get the lesson object based on the lesson_id
            lesson_obj = Lesson.objects.get(lesson_id=lesson_id)
            lesson_obj.status = "Rejected"      # update the lesson status
            lesson_obj.save()

        return redirect("admin_schedule")



def user_profile(request, username):
   
    user = get_object_or_404(User, username=username)

    tutor = None
    availability_slots = []
    if hasattr(user, 'tutor_profile'):
        tutor = user.tutor_profile  
        availability_slots = TutorAvailability.objects.filter(tutor=tutor)  

    return render(request, 'user_profile.html', {
        'user': user,
        'tutor': tutor,
        'availability_slots': availability_slots,
    })

