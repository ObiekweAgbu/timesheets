# Generated by Django 3.0.5 on 2021-05-04 15:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timesheets', '0005_holidays'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Holidays',
            new_name='Holiday',
        ),
    ]
