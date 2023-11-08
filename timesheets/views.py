from array import array
import datetime
import time
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import UpdateJob, createHoliday, createJob
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Day, Job, Profile, Total_hours
from sefas_admin.models import Customer
from datetime import datetime, timedelta
from django.views.generic import ListView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Holiday
from django.core.mail import send_mail
from django.conf import settings
from django.template import RequestContext
from django.http import Http404
from django.db.models import Sum
import calendar
from calendar import*
from datetime import datetime, timedelta
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import redirect
from bson.decimal128 import Decimal128, create_decimal128_context
from decimal import Decimal

@login_required()
def index(request):
    return render(request, 'timesheets/index.html')


@login_required()
def holidays(request):
    next = request.POST.get('next', '/holidays')

    if request.method == 'POST':

        form = createHoliday(request.POST)
        form.fields['user'].widget = forms.HiddenInput()
        form.fields['hours'].label = "Hours per day"

        if form.is_valid():
            new_set = form.save(commit=False)
            new_set.user = request.user
            date_format = "%Y-%m-%d"
            print(new_set.start_date)
            a = datetime.strptime(new_set.start_date, date_format).date()
            b = datetime.strptime(new_set.end_date, date_format).date()

            if new_set.include_weekends == False:
                daygenerator = (a + timedelta(x + 1)
                                for x in range((b - a).days))
                days = sum(1 for day in daygenerator if day.weekday() < 5)
            else:
                c = b - a
                days = c.days
            new_set.hours = float(days + 1) * float(new_set.hours)

            if (float(new_set.hours) > float(request.user.profile.holiday_remaining)):
                messages.error(request, f'This request exceeds your remaining hours')
            else:
                profile = request.user.profile
                profile.holiday_remaining = float(profile.holiday_remaining) - new_set.hours
                profile.save()
                new_set.start_date = datetime.strptime(new_set.start_date, date_format).strftime('%d-%m-%Y')
                new_set.end_date = datetime.strptime(new_set.end_date, date_format).strftime('%d-%m-%Y')
                new_set.save()
                messages.success(request, f'Holiday Requested!')
                return redirect(next)
                # send_mail(
                # 'holdiay request made',#subject
                # '',#message
                # settings.DEFAULT_FROM_USER,#from
                # ['hemery@sefas.com'],
                #  )

        # form.save()

    else:
        form = createHoliday(initial={'user': request.user})
        form.fields['user'].widget = forms.HiddenInput()
        form.fields['hours'].label = "Hours per day"
    return render(request, 'timesheets/holidays.html', {'form': form})


@login_required()
def profile(request):
    return render(request, 'timesheets/profile.html')





        
class TimesheetDetailView(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Day
    template_name = 'timesheets/timesheet.html'
    # fields =['date', 'hours'] 
    # context_object_name = 'days'
  
    def get_queryset(self):
        date_format = "%Y-%m-%d"
        result = super(TimesheetDetailView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:

            # code to return full business week from searched date 
            query = datetime.strptime(query, date_format)
            s_week, e_week = get_week_range(query)
            # print("\n \n \n \n " + query + "\n \n \n")
            # postresult = Day.objects.filter(date=query) 
            postresult = Day.objects.filter(date__range=([str(s_week), str(e_week)])).order_by('date')
            result = postresult
        else:
            result = Day.objects.order_by('date')
                    
        return result

    def get_context_data(self, **kwargs):
        context = super(TimesheetDetailView, self).get_context_data(**kwargs)
        jobs = Job.objects.filter(user = self.request.user)
        # # try:
        # hours = []
        # for day in enumerate(self.object_list):
        #         temp = Job.objects.filter(user = self.request.user, day = day.id)
        #         if temp:
        #                 day.hours = float(temp.aggregate(Sum('hours'))['hours__sum'])
        #         else:
        #             day.hours = float(0)
        #         day.save()
        context.update({
            'jobs': jobs,
            # 'hours': hours
            # 'hours': day_hours
            # 'more_context': Model.objects.all(),
        })
        return context

# get start and end dates of week from datetime object
def get_week_range(query):
    year = str(query.year)
    week = str(query.isocalendar()[1])

    s_week = datetime.strptime(f'{year}-W{int(week)}-1', "%Y-W%W-%w").date()
    e_week = s_week + timedelta(days=6.9)

    return s_week, e_week


def day_view(request, id, switch):
    template_name = 'timesheets/day_detail.html'
    query = Day.objects.filter(id = id)
    day_object = query[0]
    jobs = Job.objects.filter(day = id, user = request.user.id)
    next = request.POST.get('next', '/')
    temp = jobs.aggregate(Sum('hours'))['hours__sum']
    if switch == 0:
        if request.method == 'POST':
                form = createJob(request.POST)
                form.fields['user'].widget = forms.HiddenInput()
                form.fields['job_title'].label = "Job title"
                form.fields['customer'].label = "Customer"
                form.fields['note'].label = "Note"
                form.fields['hours'].label = "Hours"

                if form.is_valid():
                    # new_set = form.save(commit = False)
                    # temp = jobs.aggregate(Sum('hours'))['hours__sum']
                    # if temp is not None:
                    #     if temp['hours_sum'] > 7.5:
                    #         messages.error(request, f'Exceeds number of hours')
                    #     else:
                    #         new_set.save()
                    #         messages.success(request, f'Job Created!')
                    # else:
                        # hours = form.data['hours']
                        # day_object.hours += float(hours)
                        # day_object.save()
                        # print( "\n  \n \n \n \n" + hours + "\n \n \n \n \n" )
                        form.save()
                        Total_hours.objects.update_or_create(User = request.user, day = day_object, defaults={'total_hours' : temp})
                        messages.success(request, f'Job Created!')
                        return redirect(next)
                    # new_set.user = request.user
                    # date_format = "%Y-%m-%d"
                    # new_set.day = Day.objects.filter(date = datetime.strptime(
                    #         new_set.day, date_format).strftime('%d-%m-%Y'))[0]
                    # new_set.save()
        else:
            form = createJob(initial={'user': request.user})
            form.fields['user'].widget = forms.HiddenInput()
            form.fields['day'].initial = day_object
            form.fields['hours'].label = "Hours"
            form.fields['job_title'].label = "Job title"
            form.fields['customer'].label = "Customer"
            form.fields['note'].label = "Note"
    else:
        job_id = switch
        query2 = Job.objects.filter(id = job_id)
        job_object = query2[0]
        if request.method == 'POST':
                form = UpdateJob(request.POST, instance = job_object)
                # form.fields['day'].initial = day_object
                form.fields['hours'].initial = job_object.hours
                form.fields['job_title'].initial = job_object.job_title
                form.fields['customer'].initial = job_object.customer
                form.fields['note'].initial = job_object.note   
                if form.is_valid():
                    form.save()
                    messages.success(request, f'Job Updated!')
                    return redirect(next)
        else:
            form = UpdateJob(instance = job_object)

    
    # holiday name to be passed into context so template knows which job is a holiday
    customer = Customer.objects.filter(full_name  = 'Holiday')[0]
    context ={
            'day': day_object,
            'form':form,
            'jobs': jobs,
            'total' : temp,
            'customer' : customer
        }
    return render(request, template_name, context)

class my_requests(LoginRequiredMixin, ListView):
    model = Holiday
    template_name = 'timesheets/my_requests.html'
    context_object_name = 'holidays'
    ordering = ['date_requested']
    
class JobDeleteView(LoginRequiredMixin, DeleteView):
    model = Job
    context_object_name = 'job'
    template_name = 'timesheets/job_delete.html'
    # success_url = reverse_lazy('day_detail')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        total = float(Total_hours.objects.filter(day = Job.day).values_list('total_hours')[0]) - float(Job.hours)
        Total_hours.objects.update_or_create(User = request.user, day = Job.day, defaults={'total_hours' : total })
        self.object.delete()
        success_url = reverse_lazy('day_detail', args = (self.object.day.id, 0))
        # except: ("could not delete")

        return HttpResponseRedirect(success_url)    