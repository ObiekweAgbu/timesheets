# Generated by Django 3.0.5 on 2021-05-06 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0015_auto_20210506_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='holiday_remaining',
            field=models.DecimalField(decimal_places=2, default=150, max_digits=6),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='holiday_allowance',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
