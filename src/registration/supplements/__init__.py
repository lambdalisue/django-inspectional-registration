# coding=utf-8
"""
Registration Supplement
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
__all__ = ('RegistrationSupplementBase', 'get_supplement_class')
from django.core.exceptions import ImproperlyConfigured

from registration.compat import import_module
from registration.supplements.base import RegistrationSupplementBase


def get_supplement_class(path=None):
    """
    Return an instance of a registration supplement, given the dotted
    Python import path (as a string) to the supplement class.

    If the addition cannot be located (e.g., because no such module
    exists, or because the module does not contain a class of the
    appropriate name), ``django.core.exceptions.ImproperlyConfigured``
    is raised.
   
    """
    from registration.conf import settings
    path = path or settings.REGISTRATION_SUPPLEMENT_CLASS
    if not path:
        return None
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured(
                'Error loading registration addition %s: "%s"' % (module, e))
    try:
        cls = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured((
                'Module "%s" does not define a registration supplement named '
                '"%s"') % (module, attr))
    if cls and not issubclass(cls, RegistrationSupplementBase):
        raise ImproperlyConfigured((
            'Registration supplement class "%s" must be a subclass of '
            '``registration.supplements.RegistrationSupplementBase``') % path)
    return cls
