# Generated by Django 2.2.5 on 2019-09-20 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company_service', '0031_auto_20190918_1216'),
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='default_company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company_service.Company'),
        ),
    ]
