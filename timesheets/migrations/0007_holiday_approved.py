# Generated by Django 3.0.5 on 2021-05-04 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0006_auto_20210504_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='holiday',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
