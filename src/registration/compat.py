# coding=utf-8
"""
Compatibility module
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
try:
    # django 1.5, CustomUserModel
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

try:
    # django 1.4, timezone
    from django.utils.timezone import now as datetime_now
except ImportError:
    import datetime
    datetime_now = datetime.datetime.now

try:
    # django 1.4
    from django.conf.urls import url
    from django.conf.urls import patterns
    from django.conf.urls import include
except ImportError:
    from django.conf.urls.defaults import url
    from django.conf.urls.defaults import patterns
    from django.conf.urls.defaults import include

# Python 2.7 has an importlib with import_module; for older Pythons,
# Django's bundled copy provides it.
try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module

try:
    from hashlib import sha1
except ImportError:
    from django.utils.hashcompat import sha_constructor as sha1

try:
    # only available in python 2
    from django.utils.encoding import force_unicode
except ImportError:
    from django.utils.encoding import force_text as force_unicode
