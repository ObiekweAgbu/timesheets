# Generated by Django 3.2.15 on 2022-09-23 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sefas_admin', '0006_auto_20220923_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30)),
            ],
        ),
    ]
