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
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('tutor-dashboard/', views.tutor_dashboard, name='tutor_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('tutor/welcome', views.tutor_welcome, name='tutor_welcome'),
    path('tutor/dashboard', views.tutor_dashboard, name='tutor_dashboard'),
    path('tutor/lessons', views.tutor_lessons, name='tutor_lessons'),
    path('tutor/schedule', views.tutor_schedule, name='tutor_schedule'),
    path('tutor/payment', views.tutor_payment, name='tutor_payment'),
    path('requestlesson/', lesson_create_view, name='lesson_create'),
    path('student_dashboard/', student_dashboard, name='student_dashboard'),
    path('invoices/', student_invoices, name='invoices'),
    path('student_schedule/', student_schedule, name='student_schedule')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)