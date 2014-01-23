# coding=utf-8
"""
Backend

This is a modification of django-registration_ ``backends/__init__.py``
The original code is written by James Bennett

.. _django-registration: https://bitbucket.org/ubernostrum/django-registration


Original License::

    Copyright (c) 2007-2011, James Bennett
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are
    met:

        * Redistributions of source code must retain the above copyright
        notice, this list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above
        copyright notice, this list of conditions and the following
        disclaimer in the documentation and/or other materials provided
       with the distribution.
        * Neither the name of the author nor the names of other
        contributors may be used to endorse or promote products derived
        from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
    A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
    OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
__all__ = ('get_backend', 'RegistrationBackendBase')
from django.core.exceptions import ImproperlyConfigured

from registration.conf import settings
from registration.compat import import_module
from registration.backends.base import RegistrationBackendBase


def get_backend_class(path=None):
    """
    Return an class of a registration backend, given the dotted
    Python import path (as a string) to the backend class.

    If the backend cannot be located (e.g., because no such module
    exists, or because the module does not contain a class of the
    appropriate name), ``django.core.exceptions.ImproperlyConfigured``
    is raised.
    
    """
    path = path or settings.REGISTRATION_BACKEND_CLASS
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured(
                'Error loading registration backend %s: "%s"' % (module, e))
    try:
        cls = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured((
                'Module "%s" does not define a registration backend named "%s"'
                ) % (module, attr))
    if cls and not issubclass(cls, RegistrationBackendBase):
        raise ImproperlyConfigured((
                'Registration backend class "%s" must be a subclass of '
                '``registration.backends.RegistrationBackendBase``') % path)
    return cls


def get_backend(path=None):
    """
    Return an instance of a registration backend, given the dotted
    Python import path (as a string) to the backend class.

    If the backend cannot be located (e.g., because no such module
    exists, or because the module does not contain a class of the
    appropriate name), ``django.core.exceptions.ImproperlyConfigured``
    is raised.
    
    """
    return get_backend_class(path)()
