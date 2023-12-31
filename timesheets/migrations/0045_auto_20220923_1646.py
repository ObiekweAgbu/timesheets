# Generated by Django 3.2.15 on 2022-09-23 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sefas_admin', '0007_jobcode'),
        ('timesheets', '0044_alter_day_hours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='customer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sefas_admin.customer'),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_title',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sefas_admin.jobcode'),
        ),
    ]
