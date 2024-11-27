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
from tutorials.studentViews.student_dashboard import student_dashboard,lesson_create_view, student_invoices, student_schedule

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    
    # Authentication and Profile Routes
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('users/', views.UserListView.as_view(), name='user_list'),

    # Admin Routes
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/tutors', views.admin_tutors, name='admin_tutors'),
    path('admin/students', views.admin_students, name='admin_students'),
    path('admin/lessons', views.admin_lessons, name='admin_lessons'),
    path('admin/invoices', views.admin_invoices, name='admin_invoices'),
    path('admin/welcome', views.admin_welcome, name='admin_welcome'),

    # Tutor Routes
    path('tutor-dashboard/', views.tutor_dashboard, name='tutor_dashboard'),
    path('tutor/schedule', views.tutor_schedule, name='tutor_schedule'),
    path('tutor/welcome', views.tutor_welcome, name='tutor_welcome'),
    path('tutor/messages', views.tutor_messages, name='tutor_messages'),
    path('tutor/payment', views.tutor_payment, name='tutor_payment'),

    # Student Routes
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/lessons', views.student_lessons, name='student_lessons'),
    path('student/schedule', views.student_schedule, name='student_schedule'),
    path('student/payments', views.student_payments, name='student_payments'),
    path('student/messages', views.student_messages, name='student_messages'),

    # Additional Routes
    path('requestlesson/', lesson_create_view, name='lesson_create'),
    path('invoices/', student_invoices, name='invoices'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
