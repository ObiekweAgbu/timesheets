# Generated by Django 3.2.15 on 2022-09-23 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sefas_admin', '0004_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='team',
            field=models.CharField(max_length=3, primary_key=True, serialize=False),
        ),
    ]