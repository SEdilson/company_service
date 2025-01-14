# Generated by Django 2.2.5 on 2019-09-20 11:46

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=150)),
                ('permissions', models.ManyToManyField(related_name='group_permissions', to='auth.Permission')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
