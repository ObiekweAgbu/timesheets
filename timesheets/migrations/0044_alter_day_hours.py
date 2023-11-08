# Generated by Django 3.2.15 on 2022-09-23 10:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0043_auto_20220901_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='hours',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]