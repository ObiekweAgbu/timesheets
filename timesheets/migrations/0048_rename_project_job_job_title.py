# Generated by Django 3.2.15 on 2022-10-27 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0047_auto_20221026_1400'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='project',
            new_name='job_title',
        ),
    ]
