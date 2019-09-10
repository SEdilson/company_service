# Generated by Django 2.2.5 on 2019-09-09 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_service', '0016_auto_20190909_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='productionorder',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='productionorder',
            name='state',
            field=models.CharField(choices=[('Released', 'Released'), ('InProgress', 'In Progress'), ('Interrupted', 'Interrupted'), ('Done', 'Done')], default='Released', max_length=256),
        ),
    ]
