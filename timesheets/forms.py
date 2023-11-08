from calendar import Calendar
from django import forms
from django.utils.html import format_html

from sefas_admin.models import JobCode, Customer

from .models import Day, Holiday, Job
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import datetime


def less_seven(value):
    if float(value) > float(7.5):
        raise ValidationError('You cannot have more than 7.5 hours per day')


class DateInput(forms.DateInput):
    input_type = 'date'
    format = '%d/%m/%Y'


class createHoliday(forms.ModelForm):
    # user = forms.CharField(widget= forms.HiddenInput())
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)
    hours = forms.DecimalField(initial=7.5, validators=[less_seven])



    class Meta:
        model = Holiday
        fields = ['user', 'start_date', 'end_date', 'include_weekends', 'hours', 'note']

    # def clean(self):
    #     date_format = "%Y-%m-%d"
    #     a = datetime.strptime(str(self.cleaned_data['start_date']), date_format).date()
    #     b = datetime.strptime(str(self.cleaned_data['end_date']), date_format).date()
    #     c = b - a
    #     t = float(c.days + 1) *  float(self.cleaned_data['hours'])
    #     if float(t) > float(self.user.profile.holiday_remaining):
    #         print(self.cleaned_data['hours'])
    #         self.add_error('hours', format_html(
    #             'This request would take you over your allowance.'
    #             ' To add the new entry anyway, please save again.'
    #             '<input type="hidden" id="warn_hours_exceed"'  # inject hidden input with error msg itself
    #             'name="warn_hours_exceed" value="0"/>'  # so it's returned in form `data` on second save
    # How do I get outta this, What have I gotten myself into
    #         ))
class createJob(forms.ModelForm):
    # user = forms.CharField(widget= forms.HiddenInput(), initial=)
    hours = forms.DecimalField(validators=[less_seven], widget=forms.Textarea(attrs={'cols': 1, 'rows': 1}))
    day = forms.ModelChoiceField(queryset=Day.objects.order_by('date'))
    customer = forms.ModelChoiceField(queryset=Customer.objects.exclude(full_name = "Holiday" ))
    job_title = forms.ModelChoiceField(queryset=JobCode.objects.exclude(code = "Annual Leave" ))
    note = forms.CharField(required = False)
    class Meta:
        model = Job
        fields = ['user', 'day','job_title', 'customer', 'note', 'hours']

class UpdateJob(forms.ModelForm):
    hours = forms.DecimalField(initial=7.5, validators=[less_seven], widget=forms.Textarea(attrs={'cols': 1, 'rows': 1}))
    note = forms.CharField(required = False)
    customer = forms.ModelChoiceField(queryset=Customer.objects.exclude(full_name = "Holiday" ))
    job_title = forms.ModelChoiceField(queryset=JobCode.objects.exclude(code = "Annual Leave" ))
    class Meta:
        model = Job
        fields = ['job_title', 'customer', 'note', 'hours']