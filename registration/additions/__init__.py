#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
short module explanation


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
from django.db import models
from django.core.exceptions import ImproperlyConfigured

# Python 2.7 has an importlib with import_module; for older Pythons,
# Django's bundled copy provides it.
try: # pragma: no cover
    from importlib import import_module # pragma: no cover
except ImportError: # pragma: no cover
    from django.utils.importlib import import_module # pragma: no cover

def get_addition_class(path=None):
    """
    Return an instance of a registration addition, given the dotted
    Python import path (as a string) to the addition class.

    If the addition cannot be located (e.g., because no such module
    exists, or because the module does not contain a class of the
    appropriate name), ``django.core.exceptions.ImproperlyConfigured``
    is raised.
    
    """
    path = path or settings.REGISTRATION_ADDITION_CLASS
    if not path:
        return None
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error loading registration addition %s: "%s"' % (module, e))
    try:
        addition_class = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a registration addition named "%s"' % (module, attr))
    if addition_class and not issubclass(addition_class, models.Model):
        raise ImproperlyConfigured('Addition class "%s" must be a subclass of ``django.db.models.Model``' % path)
    return addition_class
