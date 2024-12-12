"""Forms for the tutorials app."""
from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from django.http import HttpRequest
from typing import Optional
from .models import User, Tutor, Student, Message, Lesson, Subjects
from django.contrib.auth.hashers import make_password

class LogInForm(forms.Form):
    """             
    Form enabling registered users to log in.        
    """

    # vincent: Docstrings on 3 lines for better readibilty (remove these comments in final version)
    # vincent: TODO: change all Docstrings to multiple lines
    # vincent: TODO: remove spacings within functions

    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def get_user(self, request) -> Optional[User]:
        """
        Returns authenticated user if possible.
        """

        user = None
        if self.is_valid():
            print("inside get_user().")
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            
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

    def clean(self) -> None:
        """Form mixing for new_password and password_confirmation fields."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')


class PasswordForm(NewPasswordMixin):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())

    def __init__(self, user=None, **kwargs) -> None:
        """Construct new form instance with a user instance."""
        
        super().__init__(**kwargs)
        self.user = user

    def clean(self) -> None:
        """Clean the data and generate messages for any errors."""

        super().clean()
        password = self.cleaned_data.get('password')
        if self.user is not None:
            user = authenticate(username=self.user.username, password=password)
        else:
            user = None
        if user is None:
            self.add_error('password', "Password is invalid")

    def save(self) -> Optional[User]:
        """Save the user's new password."""
        new_password = self.cleaned_data['new_password']
        if self.user is not None:
            self.user.set_password(new_password)
            self.user.save()
        return self.user


class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """
    Form enabling unregistered users to sign up.
    """
    class Meta:
        """Form options."""
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']  # Base fields common to both students and tutors
    def __init__(self, *args, **kwargs) -> None:
        # Get the user type if provided, for conditional fields
        self.user_type = kwargs['request'].GET.get('variations')
        self.request = kwargs.pop('request', None)  # Extract the request object
        super().__init__(*args, **kwargs)
        try:
            # retrieve the 'data' key from kwargs and extract the 'variations' parameter
            # This is used where 'data' key is used instead of 'request'
            self.user_type = kwargs['data'].GET.get('variations')
            self.request = kwargs.pop('data', None)  # Extract the request object
        except Exception as e:
            # Log the exception for debugging purposes
            print(e)
        # Add fields conditionally based on user_type
        if self.user_type == 'student':
            self.type = 'student'
            # Fields specific to students
            self.fields['date_of_birth'] = forms.DateField(required=True, label="Date of Birth")
            self.fields['proficiency_level'] = forms.ChoiceField(
                choices=Student.PROFICIENCY_LEVEL_CHOICES,
                required=True,
                label="Proficiency Level"
            )
        else:
            # no extra conditional fields for tutor sign up form
            self.type = 'tutor'

    def save(self, commit=True) -> Optional[User]:
        """
        Create a new user with optional additional processing based on user type.
        """
        # call the parent class's save method, while not commiting to the database
        user = super().save(commit=False)
        # get the user_type variation from the POST request
        variation = self.request.POST.get('variations', None)
        # set the password for user object
        user.set_password(self.cleaned_data['new_password'])
        # create a Student object if user_type variation is student
        if variation == 'student':
            student = Student.objects.create(
                username=self.cleaned_data.get('username'),      # Set username
                first_name=self.cleaned_data.get('first_name'),     # set first name
                last_name=self.cleaned_data.get('last_name'),       # set last name
                email=self.cleaned_data.get('email'),       # set email
                password=make_password(self.cleaned_data.get('new_password')),      # hash and set password
                type_of_user= 'student'   
            )
            # save the student object to database if commit is True
            if commit:
                student.save()
            return student
    
        # create a Tutor object if user_type variation is tutor
        elif variation == 'tutor':
                tutor = Tutor.objects.create(
                    username=self.cleaned_data.get('username'),     # Set username
                    first_name=self.cleaned_data.get('first_name'),     # set first name
                    last_name=self.cleaned_data.get('last_name'),       # set last name
                    email=self.cleaned_data.get('email'),           # set email
                    password=make_password(self.cleaned_data.get('new_password')),     # hash and set password
                    type_of_user= 'tutor',           
            )
                # save the tutor object to database if commit is True
                if commit:
                    tutor.save()
                return tutor

class LessonForm(forms.ModelForm):
    "Form for lessons"
    class Meta:
        model = Lesson
        fields = ['subject','frequency','term','start_time', 'day_of_week', 'duration']
    AVAILABLE_HOURS = [(f'{hour}:00', f'{hour}:00') for hour in range(9, 18)]
    # override the start_time field with a ChoiceField using the available hours
    start_time = forms.ChoiceField(
        choices=AVAILABLE_HOURS,    
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,    
    )
        
class MessageForm(forms.ModelForm):
    # define the form for the Message model
    class Meta:
        # specify the model this form is using
        model = Message
        # specify the fields to include the form
        fields = ['subject', 'content']


class UpdateSubjectsForm(forms.Form):
    subjects = forms.MultipleChoiceField(
        choices=Tutor.SUBJECTS,  
        widget=forms.CheckboxSelectMultiple, 
        required=False,
    )
    


# Vincent: TODO: are the following used??? remove if not?
