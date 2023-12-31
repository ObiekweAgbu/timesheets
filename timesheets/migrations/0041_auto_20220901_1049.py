# Generated by Django 3.2 on 2022-09-01 09:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0040_day_hours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='hours',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3, validators=[django.core.validators.MaxValueValidator(7.5), django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='job',
            name='hours',
            field=models.DecimalField(decimal_places=2, max_digits=3, validators=[django.core.validators.MaxValueValidator(7.5), django.core.validators.MinValueValidator(0.1)]),
        ),
    ]
