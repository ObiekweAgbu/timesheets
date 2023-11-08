from django.urls import path, include
from django.contrib.auth import views as auth_views
from sefas_admin import views
from .views import HolidayListView, HolidayDetailView, HolidayDeleteView, UserListView, UserDetail
from django.contrib.auth.models import User

urlpatterns = [
   # path('modify/', UserListView.as_view(), name='modify_user'),
    path('create/', views.create_user, name='create_user'),
    path('modify/', UserListView.as_view(model=User), name='modify_user'),
    path('modify/<int:pk>/', UserDetail.as_view(), name='modify_user_detail'),
    path('holidays/', HolidayListView.as_view(), name='manage_holidays'),
    path('holidays/<int:pk>/', HolidayDetailView.as_view(), name='holiday_detail'),
    path('holidays/delete/<int:pk>/', HolidayDeleteView.as_view(), name='holiday_delete'),
    path('bank_holidays/', views.bank_holidays, name='bank_holidays'),
    path('csv_report/', views.report, name='csv_report')
    #path('hlist', HolidayListView.as_view(), name='hlist'),

]