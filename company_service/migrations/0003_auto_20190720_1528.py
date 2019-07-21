# Generated by Django 2.2.3 on 2019-07-20 15:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('company_service', '0002_unitofmeasurement'),
    ]

    operations = [
        migrations.AddField(
            model_name='unitofmeasurement',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='unitofmeasurement',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]