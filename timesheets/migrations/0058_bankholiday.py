# Generated by Django 3.2.15 on 2022-11-22 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0057_delete_bankholiday'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankHoliday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timesheets.day', unique=True)),
            ],
        ),
    ]
