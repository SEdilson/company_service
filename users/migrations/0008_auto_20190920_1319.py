# Generated by Django 2.2.5 on 2019-09-20 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20190920_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(help_text='Please select only one group.', to='groups.Group'),
        ),
    ]
