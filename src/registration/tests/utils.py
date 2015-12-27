# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'


def with_apps(*apps):
    """
    Class decorator that makes sure the passed apps are present in
    INSTALLED_APPS.
    """
    from django.conf import settings
    from registration.tests.compat import override_settings
    apps_set = set(settings.INSTALLED_APPS)
    apps_set.update(apps)
    return override_settings(INSTALLED_APPS=list(apps_set))


