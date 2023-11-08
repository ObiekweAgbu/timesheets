from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls import *
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('holidays/', views.holidays, name="holidays"),
    path('my_requests/', views.my_requests.as_view(), name='my_requests'),
    path('profile/', views.profile, name="profile"),
    path('login', auth_views.LoginView.as_view(template_name='timesheets/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='timesheets/logout.html'), name='logout'),
    path('profile/', views.profile, name="profile"),
	path('timesheet/', views.TimesheetDetailView.as_view(), name="timesheet"),
    path('day_detail/<int:id>/<int:switch>/', views.day_view, name="day_detail"),
    path('jobs/delete/<int:pk>/', views.JobDeleteView.as_view(), name='job_delete'),
]