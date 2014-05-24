# coding=utf-8
"""
Compatibility module
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.conf import settings

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


# Custom User support section ==============================================={{{
#
# The following code (from === to ===) was copied from django-userena at
# 2014/05/24 to solve issue #18.
# The code is protected with BSD License.
#
# Ref: https://github.com/bread-and-pepper/django-userena/blob/master/userena/utils.py#L165-L176
#
# ---------------------------------------------------------------------------{{{
# Copyright (c) 2010, Petar Radosevic
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#     * Neither the name of the author nor the names of other
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ---------------------------------------------------------------------------}}}
#
# Django 1.5 compatibility utilities, providing support for custom User models.
# Since get_user_model() causes a circular import if called when app models are
# being loaded, the user_model_label should be used when possible, with calls
# to get_user_model deferred to execution time

user_model_label = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
    get_user_model = lambda: User
# ===========================================================================}}}
