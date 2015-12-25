# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.core.management.base import CommandError


def recall_syncdb():
    """call ``syncdb`` command to create tables of new app's models"""
    from django.core.management import call_command
    try:
        from django.db.models import loading
        loading.cache.loaded = False
    except ImportError:
        # In Django1.9, django.db.models.loading is removed
        pass
    try:
        call_command('syncdb', interactive=False, verbosity=0, migrate=False, migrate_all=True)
    except CommandError:
        # In Django1.9, syncdb command is removed
        pass


def clear_meta_caches(model):
    """clear model meta caches. it is required to refresh m2m relation"""
    CACHE_NAMES = (
            '_m2m_cache', '_field_cache', '_name_map',
            '_related_objects_cache', '_related_many_to_many_cache'
        )
    for name in CACHE_NAMES:
        if hasattr(model._meta, name):
            delattr(model._meta, name)

def clear_all_meta_caches():
    """clear all models meta caches by contenttype
    
    .. Note::
        'django.contrib.contenttypes' is required to installed

    """
    from django.contrib.contenttypes.models import ContentType
    for ct in ContentType.objects.iterator():
        clear_meta_caches(ct.model_class())

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


