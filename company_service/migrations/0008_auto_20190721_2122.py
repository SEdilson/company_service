# Generated by Django 2.2.3 on 2019-07-21 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_service', '0007_auto_20190721_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]