from django.conf import settings
from django.shortcuts import redirect

def login_prohibited(view_function):
    """Decorator for view functions that redirect users away if they are logged in."""
    
    def modified_view_function(request):
        if request.user.is_authenticated:
            if(request.user.type_of_user == 'admin'):
                return redirect(settings.REDIRECT_TO_ADMIN_WHEN_LOGGED_IN)
            elif(request.user.type_of_user == 'tutor'):
                return redirect(settings.REDIRECT_TO_TUTOR_WHEN_LOGGED_IN)
            elif(request.user.type_of_user == 'student'):
                return redirect(settings.REDIRECT_TO_STUDENT_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function