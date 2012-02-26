#!/usr/bin/env pythonh
# vim: set fileencoding=utf-8 :
"""
Automatically log activated user in when they have activated with their activation
link. This doesn't happen when the user was activated programatically with Django
Admin site.

It is originally written by 'bluejeansummer' in 
https://bitbucket.org/ubernostrum/django-registration/pull-request/5/optional-auto-login

To disable temporarily this feature, set ``False`` to ``REGISTRATION_AUTO_LOGIN``
of your ``settings.py``


.. Note::
    This feature is not available in tests because default tests of 
    django-inspectional-registration are not assumed to test with contributes.

    If you do want this feature to be available in tests, set
    ``_REGISTRATION_AUTO_LOGIN_IN_TESTS`` to ``True`` in ``setUp()`` method
    of the test case class and delete the attribute in ``tearDown()`` method.


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
import sys

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth import get_backends

from registration import setconf
from registration.signals import user_activated

setconf('REGISTRATION_AUTO_LOGIN', True)


def is_auto_login_enable():
    """get whether the registration autologin is enable"""
    if not settings.REGISTRATION_AUTO_LOGIN:
        return False
    if 'test' in sys.argv and not getattr(settings, '_REGISTRATION_AUTO_LOGIN_IN_TESTS', False):
        # Registration Auto Login is not available in test to prevent the test
        # fails of ``registration.tests.*``.
        # For testing Registration Auto Login, you must set
        # ``_REGISTRATION_AUTO_LOGIN_IN_TESTS`` to ``True``
        return False
    return True


def auto_login_reciver(sender, user, password, is_generated, request, **kwargs):
    """automatically log activated user in when they have activated"""
    if not is_auto_login_enable() or is_generated:
        # auto login feature is currently disabled by setting or
        # the user was activated programatically by Django Admin action
        # thus no auto login is required.
        return
    # A bit of a hack to bypass `authenticate()`
    backend = get_backends()[0]
    user.backend = '%s.%s' % (backend.__module__, backend.__class__.__name__)
    login(request, user)

user_activated.connect(auto_login_reciver)
