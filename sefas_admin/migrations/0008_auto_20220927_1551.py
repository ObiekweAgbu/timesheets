# Generated by Django 3.2.15 on 2022-09-27 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sefas_admin', '0007_jobcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobcode',
            name='id',
        ),
        migrations.AlterField(
            model_name='jobcode',
            name='code',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]
