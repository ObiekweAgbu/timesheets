# Generated by Django 3.2.15 on 2022-11-21 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0051_alter_holiday_hours'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankholiday',
            name='id',
            field=models.BigAutoField(auto_created=True, default=None, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bankholiday',
            name='date',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='timesheets.day'),
        ),
    ]
