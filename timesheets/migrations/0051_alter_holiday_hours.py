# Generated by Django 3.2.15 on 2022-11-01 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0050_auto_20221101_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holiday',
            name='hours',
            field=models.FloatField(),
        ),
    ]
