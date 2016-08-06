# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ('registration', '0001_initial'),
    ]
    operations = []

    if settings.REGISTRATION_SUPPLEMENT_CLASS == 'registration.supplements.default.models.DefaultRegistrationSupplement':
        operations += [
            migrations.CreateModel(
                name='DefaultRegistrationSupplement',
                fields=[
                    ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                    ('remarks', models.TextField(verbose_name='remarks')),
                ],
                options={
                },
                bases=(models.Model,),
            ),
            migrations.AddField(
                model_name='defaultregistrationsupplement',
                name='registration_profile',
                field=models.OneToOneField(editable=False, related_name='_registration_defaultregistrationsupplement_supplement', verbose_name='registration profile', to='registration.RegistrationProfile'),
                preserve_default=True,
            ),
        ]

