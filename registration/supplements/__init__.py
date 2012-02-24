#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Registration Supplement


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
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# Python 2.7 has an importlib with import_module; for older Pythons,
# Django's bundled copy provides it.
try: # pragma: no cover
    from importlib import import_module # pragma: no cover
except ImportError: # pragma: no cover
    from django.utils.importlib import import_module # pragma: no cover

from base import RegistrationSupplementBase

__all__ = ['RegistrationSupplementBase', 'get_supplement_class']

def get_supplement_class(path=None):
    """
    Return an instance of a registration supplement, given the dotted
    Python import path (as a string) to the supplement class.

    If the addition cannot be located (e.g., because no such module
    exists, or because the module does not contain a class of the
    appropriate name), ``django.core.exceptions.ImproperlyConfigured``
    is raised.
    
    """
    path = path or settings.REGISTRATION_SUPPLEMENT_CLASS
    if not path:
        return None
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error loading registration addition %s: "%s"' % (module, e))
    try:
        cls = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a registration supplement named "%s"' % (module, attr))
    if cls and not issubclass(cls, RegistrationSupplementBase):
        raise ImproperlyConfigured('Registration supplement class "%s" must be a subclass of ``registration.supplements.RegistrationSupplementBase``' % path)
    return cls
