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

#
# Django change the transaction strategy from Django 1.6
# https://docs.djangoproject.com/en/1.6/topics/db/transactions/
#
# This change cause issue #15 thus the compatibility importing is required
#
# `change_view` in Django 1.6 use transaction.atomic
# https://github.com/django/django/blob/1.6/django/contrib/admin/options.py#L1186
# `change_view` in Django 1.5 use commit_on_success
# https://github.com/django/django/blob/1.5/django/contrib/admin/options.py#L1063
#
try:
    from django.db.transaction import atomic as transaction_atomic
except ImportError:
    from django.db.transaction import commit_on_success as transaction_atomic
