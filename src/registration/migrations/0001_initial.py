# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('_status', models.CharField(editable=False, default='untreated', max_length=10, choices=[('untreated', 'Untreated yet'), ('accepted', 'Registration has accepted'), ('rejected', 'Registration has rejected')], verbose_name='status', db_column='status')),
                ('activation_key', models.CharField(null=True, default=None, verbose_name='activation key', max_length=40, editable=False)),
                ('user', models.OneToOneField(editable=False, related_name='registration_profile', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('accept_registration', 'Can accept registration'), ('reject_registration', 'Can reject registration'), ('activate_user', 'Can activate user in admin site')),
                'verbose_name': 'registration profile',
                'verbose_name_plural': 'registration profiles',
            },
            bases=(models.Model,),
        ),
    ]
