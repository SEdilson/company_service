# Generated by Django 2.2.5 on 2019-09-11 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company_service', '0029_collector_production_line'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collector',
            name='production_line',
        ),
    ]