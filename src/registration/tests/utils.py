# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'

def recall_syncdb():
    """call ``syncdb`` command to create tables of new app's models"""
    from django.db.models import loading
    from django.core.management import call_command
    loading.cache.loaded = False
    call_command('syncdb', interactive=False, verbosity=0, migrate=False, migrate_all=True)

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
