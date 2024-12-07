from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from tutorials.forms import LogInForm, PasswordForm, UserForm, SignUpForm
from tutorials.helpers import login_prohibited
from tutorials.models import User


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
        return render(request, 'tutor_dashboard.html', {'user': current_user})
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



class UserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        """Customize the queryset to fetch all users."""
        return User.objects.all()




@login_required
def tutor_dashboard(request):
    """display tutor dashboard if user is a tutor"""
    
    context = {
        'full_name': request.user.full_name(),
        'gravatar': request.user.gravatar(),
   }
    
    return render(request, 'tutor_dashboard.html', context)



#@login_required
def tutor_schedule(request):
    """schedule page for tutors"""

    context = {

    }
    return render(request, 'tutor_schedule.html', context)



class SignUpView(LoginProhibitedMixin, FormView): 
    """Display the sign-up screen and handle sign-ups."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    
    def get_form_kwargs(self):
        # Pass the 'variation' parameter as 'user_type' to the form.
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request  # Pass the request object
        # has an option of seeing a variation of the sign-up page, student or tutor
        # kwargs['user_type'] = self.request.GET.get('variation') 
        print('coming from get_form_kwargs: ', kwargs)  # Deyu: for testing
        return kwargs

    def get_context_data(self, **kwargs):
        # Add a custom message based on the user_type
        context = super().get_context_data(**kwargs)
        variation = self.request.GET.get('variation')

        if variation == 'student':
            context['message'] = "Student sign up"
            # context['message'] = "Student sign up"
        elif variation == 'tutor':
            context['message'] = "Tutor sign up"
            # context['message'] = "Tutor sign up"

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

    




