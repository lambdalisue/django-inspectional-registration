#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
"""
Automatically exected commands


AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__AUTHOR__ = "lambdalisue (lambdalisue@hashnote.net)"
from django.conf import settings
from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.db.models import signals

settings.AUTO_CREATE_USER = getattr(settings, 'AUTO_CREATE_USER', True)

if settings.DEBUG and settings.AUTO_CREATE_USER:
    # From http://stackoverflow.com/questions/1466827/ --
    #
    # Prevent interactive question about wanting a superuser created. (This code
    # has to go in this otherwise empty "models" module so that it gets processed by
    # the "syncdb" command during database creation.)
    #
    # Create our own test user automatically.
    def create_testuser(app, created_models, verbosity, **kwargs):
        USERNAME = getattr(settings, 'AUTO_CREATE_USERNAME', 'admin')
        PASSWORD = getattr(settings, 'AUTO_CREATE_PASSWORD', 'password')
        EMAIL = getattr(settings, 'AUTO_CREATE_EMAIL', 'admin@test.com')

        if getattr(settings, 'AUTO_CREATE_USER_CLASS', None):
            User = models.get_model(*settings.AUTO_CREATE_USER_CLASS.rsplit('.', 1))
        else:
            from django.contrib.auth.models import User

        try:
            User.objects.get(username=USERNAME)
        except User.DoesNotExist:
            if verbosity > 1:
                print '*' * 80
                print 'Creating test user -- login: %s, password: %s' % (USERNAME, PASSWORD)
                print '*' * 80
            assert User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
        else:
            if verbosity > 1:
                print 'Test user already exists. -- login: %s, password: %s' % (USERNAME, PASSWORD)
    signals.post_syncdb.disconnect(
        create_superuser,
        sender=auth_models,
        dispatch_uid='django.contrib.auth.management.create_superuser')
    signals.post_syncdb.connect(create_testuser,
        sender=auth_models, dispatch_uid='common.models.create_testuser')
