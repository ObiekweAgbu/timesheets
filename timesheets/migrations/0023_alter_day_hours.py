# Generated by Django 3.2 on 2022-07-25 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0022_alter_timesheet_total_hours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='hours',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
