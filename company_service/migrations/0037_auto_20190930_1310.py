# Generated by Django 2.2.5 on 2019-09-30 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company_service', '0036_stopnotification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stopnotification',
            name='stop_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='company_service.StopCode'),
        ),
    ]