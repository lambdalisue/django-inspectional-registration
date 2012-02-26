#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Utilities for django-inspectional-registration


METHODS:
    generate_activation_key
        generate activation key via username originally written by 
        James Bennett in django-registration

    generate_random_password
        generate random password with passed password length

    send_mail
        send mail to recipients. use django-mailer ``send_mail`` method 
        when possible

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
import random

from django.contrib.sites.models import Site
from django.contrib.sites.models import RequestSite
from django.utils.hashcompat import sha_constructor

def get_site(request):
    """get current ``django.contrib.Site`` instance

    return ``django.contrib.RequestSite`` instance when the ``Site`` is
    not installed.

    """
    if Site._meta.installed:
        return Site.objects.get_current()
    else:
        return RequestSite(request)

def generate_activation_key(username):
    """generate activation key with username
    
    originally written by ubernostrum in django-registration_

    .. _django-registration: https://bitbucket.org/ubernostrum/django-registration
    """
    if isinstance(username, unicode):
        username = username.encode('utf-8')
    salt = sha_constructor(str(random.random())).hexdigest()[:5]
    activation_key = sha_constructor(salt+username).hexdigest()
    return activation_key

def generate_random_password(length=10):
    """generate random password with passed length"""
    # Without 1, l, O, 0 because those character are hard to tell
    # the difference between in same fonts
    chars = '23456789abcdefghijklmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
    password = "".join([random.choice(chars) for i in xrange(length)])
    return password

def send_mail(subject, message, from_email, recipients):
    """send mail to recipients
    
    this method use django-mailer_ ``send_mail`` method when
    the app is in ``INSTALLED_APPS``

    .. Note::
        django-mailer_ ``send_mail`` is not used duaring unittest
        because it is a little bit difficult to check the number of
        mail sent in unittest for both django-mailer and original
        django ``send_mail``

    .. _django-mailer: http://code.google.com/p/django-mailer/
    """
    from django.conf import settings
    from django.core.mail import send_mail as django_send_mail
    import sys
    if 'test' not in sys.argv and 'mailer' in settings.INSTALLED_APPS:
        try:
            from mailer import send_mail
            return send_mail(subject, message, from_email, recipients)
        except ImportError:
            pass
    return django_send_mail(subject, message, from_email, recipients)
