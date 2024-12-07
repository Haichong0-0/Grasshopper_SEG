"""Forms for the tutorials app."""
from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from .models import User, Tutor, Student, Message
from django.contrib.auth.hashers import make_password
from datetime import date, timedelta
from .models import Lesson


class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def get_user(self, request):
        """Returns authenticated user if possible."""

        user = None
        if self.is_valid():
            print("inside get_user().")
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            print("get_user(): ", username, password)
            
            user = authenticate(request=request, username=username, password=password)
            print(user)
        return user


class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'date_of_birth']

class NewPasswordMixin(forms.Form):
    """Form mixing for new_password and password_confirmation fields."""

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Form mixing for new_password and password_confirmation fields."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')


class PasswordForm(NewPasswordMixin):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())

    def __init__(self, user=None, **kwargs):
        """Construct new form instance with a user instance."""
        
        super().__init__(**kwargs)
        self.user = user

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        password = self.cleaned_data.get('password')
        if self.user is not None:
            user = authenticate(username=self.user.username, password=password)
        else:
            user = None
        if user is None:
            self.add_error('password', "Password is invalid")

    def save(self):
        """Save the user's new password."""

        new_password = self.cleaned_data['new_password']
        if self.user is not None:
            self.user.set_password(new_password)
            self.user.save()
        return self.user


class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']  # Base fields common to both students and tutors

    def __init__(self, *args, **kwargs):
        # Get the user type if provided (for conditional fields)
        self.user_type = kwargs['request'].GET.get('variations')
        self.request = kwargs.pop('request', None)  # Extract the request object
        super().__init__(*args, **kwargs)

        try:
            self.user_type = kwargs['data'].GET.get('variations')
            self.request = kwargs.pop('data', None)  # Extract the request object
        # self.user_type = kwargs['request'].GET.get('variations')

        except Exception as e:
            print(e)

        # Add fields conditionally based on user_type
        if self.user_type == 'student':
            self.type = 'student'
            # Fields specific to students
            self.fields['date_of_birth'] = forms.DateField(required=True, label="Date of Birth")
            # self.fields['subjects'] = forms.CharField(max_length=100, required=True, label="Subjects")
            self.fields['proficiency_level'] = forms.ChoiceField(
                choices=Student.PROFICIENCY_LEVEL_CHOICES,
                required=True,
                label="Proficiency Level"
            )
        else:
            self.type = 'tutor'

    def save(self, commit=True):
        """Create a new user with optional additional processing based on user type."""
        user = super().save(commit=False)
        variation = self.request.POST.get('variations', None)

        user.set_password(self.cleaned_data['new_password'])

        if variation == 'student':
            print ("student object being initialised.")
            student = Student.objects.create(
                username=self.cleaned_data.get('username'),
                first_name=self.cleaned_data.get('first_name'),
                last_name=self.cleaned_data.get('last_name'),
                email=self.cleaned_data.get('email'),
                password=make_password(self.cleaned_data.get('new_password')),
                type_of_user= 'student'
                # type_of_user=self.cleaned_data.get('variations'),
            )
            print("Student object created: ", student)

            if commit:
                student.save()
            print("Student object created: ", student)
            return student
    
        elif variation == 'tutor':
                print ("Creating a Tutor object...")
                tutor = Tutor.objects.create(
                    username=self.cleaned_data.get('username'),
                    first_name=self.cleaned_data.get('first_name'),
                    last_name=self.cleaned_data.get('last_name'),
                    email=self.cleaned_data.get('email'),
                    password=make_password(self.cleaned_data.get('new_password')),     
                type_of_user= 'tutor',
                    # type_of_user=self.cleaned_data.get('variations'),
            )

                if commit:
                    tutor.save()
                print("Tutor object created: ", tutor)
                return tutor
    

class LessonForm(forms.ModelForm):
    "Form for lessons"
    class Meta:
        model = Lesson
        fields = ['subject','frequency','term','start_time', 'duration']
    AVAILABLE_HOURS = [(f'{hour}:00', f'{hour}:00') for hour in range(9, 18)]
    start_time = forms.ChoiceField(
        choices=AVAILABLE_HOURS,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )
        
class MessageForm(forms.ModelForm):
    tutor_name = forms.CharField(max_length=255, required=True, label="Tutor Name")
    class Meta:
        model = Message
        fields = ['subject', 'content']


""""search form for search bar in dashboards"""
class SearchForm(forms.ModelForm):
    query = forms.CharField(max_length=100, required=False, label="Search Here")
