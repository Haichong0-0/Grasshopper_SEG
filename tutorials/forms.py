"""Forms for the tutorials app."""
from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from .models import User, Tutor, Student

###################################################
'''from .models import Admin, Tutor, Student, Lesson, Invoice'''
###################################################

class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def get_user(self):
        """Returns authenticated user if possible."""

        user = None
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
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
        variation = self.request.POST.get('variations')

        user.set_password(self.cleaned_data['new_password'])

        user = User.objects.create_user(
            username=self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('new_password'),
            type_of_user= variation if variation else 'student'
        )
        
        if commit:
            user.save()

        return user
    



'''class AdminForm(forms.ModelForm):
    """Form for admins"""

    class Meta:

        model = Admin
        fields = '__all__'


class TutorForm(forms.ModelForm):
    "Form for tutors"

    class Meta:

        model = Tutor
        fields = '__all__'


class StudentForm(forms.ModelForm):
    "Form for admins"

    class Meta:

        model = Student
        fields = '__all__'


class LessonForm(forms.ModelForm):
    "Form for lessons"

    class Meta:

        model = Lesson
        fields = '__all__'

class InvoiceForm(forms.ModelForm):
    "Form for invoices"

    class Meta:

        model = Invoice
        fields = '__all__'''
