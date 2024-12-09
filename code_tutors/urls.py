"""
URL configuration for code_tutors project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from tutorials import views
from tutorials.studentViews.student_dashboard import student_dashboard,lesson_create_view, student_invoices, student_schedule, student_welcome
from tutorials.tutorViews.tutor_dashboard import tutor_schedule, tutor_lessons, tutor_payments # vincent TODO: remove in final version??
from tutorials.views import leave_message

urlpatterns = [
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('admin/', admin.site.urls),        # default django built-in admin page
    path('', views.home, name='home'),
    # path('dashboard/', views.dashboard, name='dashboard'),            # vincent TODO: delete in final version
    path('code_admin/welcome', views.admin_welcome, name='admin_welcome'),       # custom admin page
    path('code_admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('code_admin/dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('code_admin/lessons', views.admin_lessons, name='admin_lessons'),
    path('code_admin/schedule', views.admin_schedule, name='admin_schedule'),
    path('code_admin/messages', views.admin_messages, name='admin_messages'),
    path('code_admin/payment', views.admin_payment, name='admin_payment'),
    path('tutor-dashboard/', views.tutor_dashboard, name='tutor_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('tutor/welcome', views.tutor_welcome, name='tutor_welcome'),
    path('tutor/dashboard', views.tutor_dashboard, name='tutor_dashboard'),
    path('tutor/lessons', views.tutor_lessons, name='tutor_lessons'),
    path('tutor/schedule', views.tutor_schedule, name='tutor_schedule'),
    path('tutor/payment', views.tutor_payment, name='tutor_payment'),
    path('requestlesson/', lesson_create_view, name='lesson_create'), 
    path('student_dashboard/', student_dashboard, name='student_dashboard'),
    path('invoices/', student_invoices, name='invoices'),
    path('student_schedule/', student_schedule, name='student_schedule'),
    path('lesson/<int:lesson_id>/confirm_class/', views.ConfirmClassView.as_view(), name='confirm_class'),
    path('lesson/<int:lesson_id>/reject_class/', views.RejectClassView.as_view(), name='reject_class'),    
    path('student_welcome/', student_welcome, name='student_welcome'),
    path('leave-message/', leave_message, name='leave_message'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)