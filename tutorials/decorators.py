from functools import wraps
from django.shortcuts import render

def user_type_required(user_type):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            print("User:", request.user, request.user.type_of_user)
            if getattr(request.user, 'type_of_user', None) == user_type:
                return view_func(request, *args, **kwargs)
            return render(request, 'unauthorized_page.html')
        return _wrapped_view
    return decorator