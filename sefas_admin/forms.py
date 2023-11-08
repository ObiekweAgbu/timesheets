from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from timesheets.models import Holiday, Profile, HolidayStatus


class DateInput(forms.DateInput):
    input_type = 'date'
    format = '%d/%m/%Y'
    
class UserCreateForm(UserCreationForm):
    is_superuser = forms.CheckboxInput()
    is_staff = forms.CheckboxInput()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'password1', 'password2']

    if (is_staff):
        User.is_superuser = True

class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        total_hours = forms.DecimalField(max_digits=10, decimal_places=2)
        holiday_allowance = forms.DecimalField(decimal_places=2, max_digits=6)
        holiday_remaining = forms.DecimalField(decimal_places=2, max_digits=6)
        holiday_awaiting_approval = forms.DecimalField(decimal_places=2, max_digits=6)
        fields = ['team', 'holiday_allowance', 'holiday_remaining', 'holiday_awaiting_approval']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        holiday_allowance = forms.DecimalField(decimal_places=2, max_digits=6)
        holiday_remaining = forms.DecimalField(decimal_places=2, max_digits=6)
        fields = ['team', 'holiday_allowance', 'holiday_remaining']

class UpdateUserForm(forms.ModelForm):
    is_superuser = forms.CheckboxInput()
    is_staff = forms.CheckboxInput()
    is_active = forms.CheckboxInput()
    class Meta:
        model = User
        fields = ['username', 'is_staff', 'is_superuser', 'is_active', 'password']

class ApproveHoliday(forms.ModelForm):

    class Meta:
        model = Holiday
        fields = ['approved']

class DateRangeForm(forms.Form):
    date_from = forms.DateField(widget=DateInput)
    date_to = forms.DateField(widget=DateInput)