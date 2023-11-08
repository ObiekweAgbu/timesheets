# Generated by Django 3.2.13 on 2022-07-25 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sefas_admin', '0003_team'),
        ('timesheets', '0020_auto_20220725_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='hours',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='holiday',
            name='approved',
            field=models.CharField(choices=[('0', 'PENDING'), ('1', 'APPROVED'), ('2', 'REJECTED')], default='0', max_length=1),
        ),
        migrations.AlterField(
            model_name='holiday',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sefas_admin.team'),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='total_hours',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.DeleteModel(
            name='Dog',
        ),
    ]
