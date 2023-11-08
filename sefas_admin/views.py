from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from .forms import *
from django.contrib.auth.decorators import user_passes_test 
from timesheets.models import Day, Holiday, Job
from sefas_admin.models import Customer, JobCode, Team
from django.views.generic import ListView, DeleteView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from timesheets.models import BankHoliday
from .models import Team
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from dateutil import parser
from timesheets import *
from bson.decimal128 import Decimal128, create_decimal128_context
from decimal import Decimal
import csv
import pandas
import urllib.request, json 
# my_app/management/commands/my_custom_startup_command.py

from django.core.management.base import BaseCommand, CommandError


class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    if request.method == 'POST':

        form = UserCreateForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}!')
    else:
        form = UserCreateForm()
    return render(request, 'sefas_admin/create_user.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def bank_holidays(request):
    BH = BankHoliday.objects.all().order_by('day__date')
    pag = Paginator(BH, 10)
    pn = request.GET.get('page')
    page = pag.get_page(pn)
    if request.method == 'POST':
        # try:
        
        #     User = get_user_model()
        #     users = User.objects.all()
        #     for user in users:
        #         for bankhol in BankHoliday.objects.all:
        #             if not Job.objects.filter(job_title = bankhol.title):
        #                 Job.objects.create(day = )
        #         # current =  datetime.today()
        #         # for x in range (0, 365):
        #         #     next_date = current + timedelta(days=x)
        #         #     if next_date.weekday() <= 4 and not Day.objects.filter(date=next_date)[0]:
        #         #            Day.objects.create(date=next_date.strftime('%Y-%m-%d'), hours=0.0)
        # except:
        #     raise CommandError('Initalization failed.')
        # temp = request.GET.get('https://www.gov.uk/bank-holidays.json')
        # with urllib.request.urlopen('https://www.gov.uk/bank-holidays.json') as url:
        #         bhols = json.load(url)
        #         print(url)
   
        #print(bhols['england-and-wales'])
        # BankHoliday.objects.all().delete()
        # for hol in bhols['england-and-wales']['events']:
        for hol in BankHoliday.objects.all:
            # BankHoliday.objects.create(title=hol['title'], date=hol['date'])
            # temp = parser.parse(hol['date'])
            # dayt = temp.strftime('%d-%m-%Y')
            # print(dayt)
            #check if job is created for bank holiday and if not create one
            # if not Job.objects.filter(day = Day.objects.filter(date = hol['date'])[0], job_title= Job.objects.filter(code = "National Holiday")[0]).exists():
            Job.objects.create(day = Day.objects.filter(date = hol.date )[0], job_title= Job.objects.filter(code = "National Holiday")[0], customer= Customer.objects.filter(full_name = "Holiday")[0], hours = 7.5, note = hol.title)
         
    return render(request, 'sefas_admin/bank_holidays.html', {'BH':page})
    

@user_passes_test(lambda u: u.is_superuser)
def update_user(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = UpdateUserForm()
    return render(request, 'sefas_admin/update_user.html', {'form': form})

# def HolidayListView(request):
#     if request.method == 'POST':
#         form = ApproveHoliday(request.POST, instance=request.holiday)
#         if form.is_valid():
#             form.save()
#     else:
#         form = ApproveHoliday
#     return render(request, 'sefas_admin/manage_holidays.html', {'form': form})

class UserListView(AdminStaffRequiredMixin, ListView):

    model = User
    context_object_name = 'users'
    template_name = 'sefas_admin/user_list.html'
    ordering = ['id']
    queryset = User.objects.all()
    def get_queryset(self):
        result = super(UserListView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            postresult = User.objects.filter(username__icontains=query)
            result = postresult
        else:
            result = User.objects.all()
        return result


class HolidayListView(AdminStaffRequiredMixin, ListView):
    model = Holiday
    template_name = 'sefas_admin/manage_holidays.html'
    context_object_name = 'holidays'
    ordering = ['date_requested']
    #paginate_by = 10

    def get_queryset(self):
        result = super(HolidayListView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            postresult = Holiday.objects.filter(user__username__icontains=query) | Holiday.objects.filter(start_date__icontains=query) | Holiday.objects.filter(end_date__icontains=query)
            result = postresult
        else:
            result = Holiday.objects.all()
        return result

class HolidayDetailView(AdminStaffRequiredMixin, UpdateView):
    model = Holiday
    fields = ['approved']
    context_object_name = 'holidays'
    template_name = 'sefas_admin/holiday_detail.html'
    success_url = reverse_lazy('manage_holidays')

class HolidayDeleteView(AdminStaffRequiredMixin, DeleteView):
    model = Holiday
    context_object_name = 'holiday'
    template_name = 'sefas_admin/holiday_delete.html'
    success_url = reverse_lazy('manage_holidays')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        profile = self.request.user.profile
        profile.holiday_remaining = float(profile.holiday_remaining) +  float(self.object.hours)
        profile.save()
        self.object.delete()
        format = '%d-%m-%Y'
        sdate = datetime.strptime(str(self.object.start_date), format)
        edate = datetime.strptime(str(self.object.end_date), format) + timedelta(days=1)
        day_list = pandas.date_range(sdate,edate-timedelta(days=1),freq='B')
        if self.object.approved == HolidayStatus.APPROVED:
            for dayt in day_list:
                    print(str(dayt))
                    Job.objects.filter(day = Day.objects.filter(date = dayt)[0], customer = Customer.objects.filter(customer= "LVE")[0])[0].delete()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

class UserDetail(AdminStaffRequiredMixin, UpdateView):
    model = User
    context_object_name = 'User'
    fields=['first_name', 'last_name', 'is_staff', 'is_superuser', 'password']
    template_name = 'sefas_admin/update_user.html'
    success_url = reverse_lazy('modify_user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileUpdateForm()
        context['profile_form'].fields['team'].initial = context['User'].profile.team
        context['profile_form'].fields['holiday_allowance'].initial = context['User'].profile.holiday_allowance
        context['profile_form'].fields['holiday_remaining'].initial = context['User'].profile.holiday_remaining
        # context['profile_form'] = context['User'].profile
        context['teams'] = Team.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        profile = self.object.profile
        team = self.get_context_data()['teams'].filter(team=request.POST['team']).first()
        profile.team = team
        profile.holiday_allowance = request.POST['holiday_allowance']
        profile.holiday_remaining = request.POST['holiday_remaining']
        profile.save()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

@user_passes_test(lambda u: u.is_superuser) 
def report(request):
    jobs = Job.objects.order_by('day')
    pag = Paginator(jobs, 10)
    pn = request.GET.get('page')
    page = pag.get_page(pn)
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            try:
                start = form.cleaned_data['date_from']
                end = form.cleaned_data['date_to']
                data = download_csv(request, Job.objects.filter(day__in=Day.objects.filter(date__range=([str(start), str(end)]))))
            except:
                data = download_csv(request, Job.objects.all)  
                data.short_description = "Download selected as csv"
            response = HttpResponse(data, content_type='text/csv')
            return response     
    else:
        form = DateRangeForm(request.POST)
    return render(request, 'sefas_admin/csv_report.html', {'jobs':page})

@user_passes_test(lambda u: u.is_superuser) 
def download_csv(request, queryset):
    opts = queryset.model._meta
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response
download_csv.short_description = "Download selected as csv"
