# Generated by Django 3.2.15 on 2022-11-01 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0049_auto_20221031_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='holiday_allowance',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='holiday_awaiting_approval',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='holiday_remaining',
            field=models.FloatField(),
        ),
    ]