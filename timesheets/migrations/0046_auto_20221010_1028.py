# Generated by Django 3.2.15 on 2022-10-10 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0045_auto_20220923_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holiday',
            name='hours',
            field=models.FloatField(),
        ),
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