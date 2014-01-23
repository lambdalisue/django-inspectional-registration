# coding=utf-8
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
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import sys
from django.contrib.auth import login
from django.contrib.auth import get_backends
from registration.signals import user_activated
from registration.contrib.autologin.conf import settings


def is_auto_login_enable():
    """get whether the registration autologin is enable"""
    if not settings.REGISTRATION_AUTO_LOGIN:
        return False
    if 'test' in sys.argv and not getattr(settings,
                                          '_REGISTRATION_AUTO_LOGIN_IN_TESTS',
                                          False):
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
