from djongo import models
from django.contrib.auth.models import User

class Team(models.Model):
    team = models.CharField(max_length=2, primary_key=True)
    full_name = models.CharField(max_length=30)
    manager = models.ForeignKey(User, limit_choices_to={'is_staff' : True}, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.full_name}'

class Customer(models.Model):
    customer = models.CharField(max_length=3,primary_key=True)
    full_name = models.CharField(max_length=30)

    class Meta:
        ordering = ('full_name',)

    def __str__(self):
        return f'{self.full_name}'

class JobCode(models.Model):
    code = models.CharField(max_length=30, primary_key=True)

    class Meta:
        ordering = ('code',)
        
    def __str__(self):
        return f'{self.code}'

