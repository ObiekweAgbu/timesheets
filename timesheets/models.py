# from django.db import models
from djongo import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.conf import settings
from sefas_admin.models import Customer, JobCode, Team
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from django.urls import resolve
from datetime import date, datetime
import calendar
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Sum
from datetime import date, timedelta
import pandas 
class HolidayStatus(models.TextChoices):
    PENDING = 0, 'PENDING'
    APPROVED = 1, 'APPROVED'
    REJECTED = 2, 'REJECTED'




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # team = models.CharField(max_length=10)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    # holiday_allowance = models.DecimalField(decimal_places=2, max_digits=6)
    # holiday_remaining = models.DecimalField(decimal_places=2, max_digits=6)
    # holiday_awaiting_approval = models.DecimalField(
    #     decimal_places=2, max_digits=6)
    holiday_allowance = models.FloatField()
    holiday_remaining = models.FloatField()
    holiday_awaiting_approval = models.FloatField()

    def __str__(self):
        return f'{self.user.username}'


class Holiday(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # user = models.CharField(max_length=50)
    start_date = models.CharField(max_length=20)
    # start_date=models.DateField()
    # end_date=models.DateField()
    end_date = models.CharField(max_length=20)
    hours = models.FloatField()
    date_requested = models.DateTimeField(auto_now_add=True)
    approved = models.CharField(
        choices=HolidayStatus.choices, default=HolidayStatus.PENDING, max_length=1)
    # approved = models.IntegerField(choices=HolidayStatus.choices, default=HolidayStatus.PENDING)
    # approved = models.BooleanField(default=False)
    note = models.CharField(max_length=50, default="", blank=True)
    include_weekends = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} {self.id}'

    # def save_model(self, request, obj, form, change):
    #     update_fields = []
    #     if change:
    #         if form.initial['approved'] != form.cleaned_data['approved']:
    #             if form.cleaned_data['approved'] == True:
    #                 update_fields.append('approved')
    #             else:
    #                 update_fields.append('un-approved')
    #
    #     obj.save(update_fields=update_fields)


def create_Holiday(sender, instance, **kwargs):
    # print (kwargs)
    if kwargs['created']:
        print("CREATED")
        # print(instance.user.username)
        # send_email(instance.user.username)
        # holiday_request_email(instance)

    else:
        print(instance.approved)
        if (instance.approved == '1'):
            print("APPROVED")
            format = '%d-%m-%Y'
            sdate = datetime.strptime(str(instance.start_date), format)
            edate = datetime.strptime(str(instance.end_date), format) + timedelta(days=1)
            # day_list = pandas.date_range(sdate,edate-timedelta(days=1),freq='B')
            day_list = pandas.date_range(sdate,edate-timedelta(days=1),freq='B')
            for dayt in day_list:
                print(str(dayt))
                Job.objects.create(user = instance.user, day = Day.objects.filter(date = dayt)[0], job_title = JobCode.objects.filter(code = "Annual Leave")[0], customer = Customer.objects.filter(customer = "LVE")[0], note = instance.note, hours = float(instance.hours)/len(day_list))

            # send_single_mail(instance, 'APPROVED')
        elif (instance.approved == '2'):
            print("REJECTED")
            # send_single_mail(instance, 'REJECTED')


post_save.connect(create_Holiday, Holiday)


def delete_Holiday(sender, **kwargs):
    print("DELETED")



post_delete.connect(delete_Holiday, Holiday)


def create_profile(sender, instance, **kwargs):
    if kwargs['created']:
        team = Team.objects.get(pk=settings.DEFAULT_TEAM)
        Profile.objects.create(user=instance, team=team, holiday_allowance=settings.DEFAULT_HOL_AMOUNT,
                               holiday_remaining=settings.DEFAULT_HOL_AMOUNT, holiday_awaiting_approval=0)


post_save.connect(create_profile, sender=User)


def send_single_mail(holiday, type):
    messages = []

    usermsg = MIMEMultipart('mixed')
    usermsg['From'] = settings.EMAIL_FROM
    usermsg['To'] = holiday.user.username
    usermsg['Subject'] = 'Holiday Request ' + type
    text = str(holiday.user.first_name) + ', your request from the ' + str(holiday.start_date) + ' to ' + str(
        holiday.end_date) + ' has been ' + type + '.'
    usermsg.attach(MIMEText(text))
    messages.append(usermsg)

    send_email(messages)


def holiday_request_email(holiday):
    messages = []

    usermsg = MIMEMultipart('mixed')
    usermsg['From'] = settings.EMAIL_FROM
    usermsg['To'] = holiday.user.username
    usermsg['Subject'] = 'Holiday Request Submitted'
    text = str(holiday.user.first_name) + ', your request from the ' + str(holiday.start_date) + ' to ' + str(
        holiday.end_date) + ' for ' + str(holiday.hours) + ' hours has been submitted.'
    usermsg.attach(MIMEText(text))
    messages.append(usermsg)

    manmsg = MIMEMultipart('mixed')
    manmsg['From'] = settings.EMAIL_FROM
    manmsg['To'] = holiday.user.profile.team.manager.username
    manmsg['Subject'] = 'Holiday Request Submitted - ' + \
        holiday.user.first_name + ' ' + holiday.user.last_name
    text = str(holiday.user.username) + ' has submitted a holiday request from: ' + str(
        holiday.start_date) + ' to ' + str(holiday.end_date) + ' for a total of ' + str(holiday.hours) + ' hours. See this at http://127.0.0.1:8000/sefas_admin/holidays/' + str(holiday.id)
    manmsg.attach(MIMEText(text))
    messages.append(manmsg)

    send_email(messages)


def send_email(messages):
    smtp = smtplib.SMTP()
    smtp.set_debuglevel(True)
    smtp.connect(settings.EMAIL_HOST)

    for msg in messages:
        smtp.sendmail(msg['From'], msg['To'], msg.as_string())

    smtp.quit()


project_tasks = (
    (10, "It's life-sustaining billable work!"),
    (10, "It's signing new business!"),
    (5, "It's publishable code! Ship it!"),
    (5, "It's sharp visual desgin! Show it!"),
    (5, "It's concrete planning or accounting!"),
    (2, "It's new self-promotion!"),
    (2, "It's a new article for the blog!"),
    (2, "It's a social or business development!"),
    (1, "It's maintaining an old relationship!"),
    (1, "It's making a new relationship!")
)

def total_hours(object1, object2):
    try:
        object1.hours = object2.objects.all().aggregate(Sum('hours')['hours__sum'])

    except: ValidationError("Sum of all day hours should not be greater than 7.5")

def validate_job(value, object1, object2):
    if value != object1:
        return value
    else:
        raise ValidationError("Sum of all day hours should not be greater than 7.5")

# class Timesheet (models.Model):
#     user = models(User, on_delete=models.CASCADE)
#     total_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
#     team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
#     date_added = models.DateTimeField(auto_now_add=True)
#     date_modified = models.DateTimeField(auto_now=True)
 

#     def __str__(self):
#         return f'{self.user.username} {self.id}'

#     def __unicode__(self):
#         return u"%s %s - %s" % (self.user.first_name, self.user.last_name, self.total_hours)


class Day (models.Model):
    date = models.DateField(unique = True)
    hours = models.ManyToManyRel(validators=[
                                 MinValueValidator(0.0)], default = 0.0)

    def __str__(self):
        return f'{self.date}'

class BankHoliday(models.Model):
    title = models.CharField(max_length=50)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.day}'

class Total_hours(models.Model):
    user =  user = models.ForeignKey(User, on_delete=models.CASCADE, default = None)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    total_hours = models.FloatField()
 

class Job (models.Model):
    user =  user = models.ForeignKey(User, on_delete=models.CASCADE, default = None)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    job_title = models.ForeignKey(JobCode, on_delete=models.CASCADE, default = None )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default = None )
    note = models.CharField(max_length=500)
    hours = models.FloatField(validators=[
                                MaxValueValidator(7.5), MinValueValidator(0.1)])

    def __str__(self):
        return f'{self.job_title} {self.customer} {self.note}'
