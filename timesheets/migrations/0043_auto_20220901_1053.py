# Generated by Django 3.2 on 2022-09-01 09:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0042_auto_20220901_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='hours',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MaxValueValidator(7.5), django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='job',
            name='hours',
            field=models.FloatField(validators=[django.core.validators.MaxValueValidator(7.5), django.core.validators.MinValueValidator(0.1)]),
        ),
    ]
