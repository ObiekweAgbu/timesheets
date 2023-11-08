# Generated by Django 3.2.15 on 2022-11-22 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0054_rename_date_bankholiday_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankholiday',
            name='id',
        ),
        migrations.AlterField(
            model_name='bankholiday',
            name='day',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='timesheets.day'),
        ),
    ]
