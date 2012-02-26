#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Default registration backend class

This is a modification of django-registration_ ``admin.py``
The original code is written by James Bennett

.. _django-registration: https://bitbucket.org/ubernostrum/django-registration


AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

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
import sys

from django.conf import settings
from django.core.urlresolvers import reverse

from ..base import RegistrationBackendBase
from ... import signals
from ...models import RegistrationProfile
from ...forms import ActivationForm
from ...forms import RegistrationForm
from ...supplements import get_supplement_class

class DefaultRegistrationBackend(RegistrationBackendBase):
    """Default registration backend class

    A registration backend which floows a simple workflow:

    1.  User sigs up, inactive account with unusable password is created.

    2.  Inspector accept or reject the account registration.

    3.  Email is sent to user with/without activation link (without when rejected)

    4.  User clicks activation link, enter password, account is now active

    Using this backend requires that

    *   ``registration`` be listed in the ``INSTALLED_APPS`` settings
        (since this backend makes use of models defined in this application).

    *   ``django.contrib.admin`` be listed in the ``INSTALLED_APPS`` settings

    *   The setting ``ACCOUNT_ACTIVATION_DAYS`` be supplied, specifying (as an
        integer) the number of days from acception during which a user may 
        activate their account (after that period expires, activation will be
        disallowed). Default is ``7``

    *   The creation of the templates

        -   ``registration/registration_email.txt``
        -   ``registration/registration_email_subject.txt``
        -   ``registration/acception_email.txt``
        -   ``registration/acception_email_subject.txt``
        -   ``registration/rejection_email.txt``
        -   ``registration/rejection_email_subject.txt``
        -   ``registration/activation_email.txt``
        -   ``registration/activation_email_subject.txt``

    Additinally, registration can be temporarily closed by adding the setting
    ``REGISTRATION_OPEN`` and setting it to ``False``. Omitting this setting, or
    setting it to ``True``, will be imterpreted as meaning that registration is
    currently open and permitted.

    Internally, this is accomplished via storing an activation key in an instance
    of ``registration.models.RegistrationProfile``. See that model and its custom
    manager for full documentation of its fields and supported operations.

    """

    def register(self, username, email, request, send_email=None):
        """register new user with ``username`` and ``email``

        Given a username, email address, register a new user account, which will
        initially be inactive and has unusable password.

        Along with the new ``User`` object, a new
        ``registration.models.RegistrationProfile`` will be created, tied to that
        ``User``, containing the inspection status and activation key which will
        be used for this account (activation key is not generated untill its
        inspection status is set to ``accepted``)

        An email will be sent to the supplied email address; The email will be
        rendered using two templates. See the documentation for
        ``RegistrationProfile.send_registration_email()`` for information about
        these templates and the contexts provided to them.

        If ``REGISTRATION_REGISTRATION_EMAIL`` of settings is ``None``, no 
        registration email will be sent.

        After the ``User`` and ``RegistrationProfile`` are created and the
        registration email is sent, the signal
        ``registration.signals.user_registered`` will be sent, with the new
        ``User`` as the keyword argument ``user``, the ``RegistrationProfile``
        of the new ``User`` as the keyword argument ``profile`` and the class
        of this backend as the sender.

        """
        if send_email is None:
            send_email = settings.REGISTRATION_REGISTRATION_EMAIL

        new_user = RegistrationProfile.objects.register(
                username, email, self.get_site(request),
                send_email=send_email)

        signals.user_registered.send(
                sender=self.__class__,
                user=new_user,
                profile=new_user.registration_profile,
                request=request,
            )

        return new_user

    def accept(self, profile, request, send_email=None, message=None):
        """accept the account registration of ``profile``

        Given a profile, accept account registration, which will
        set inspection status of ``profile`` to ``accepted`` and generate new
        activation key of ``profile``.

        An email will be sent to the supplied email address; The email will be
        rendered using two templates. See the documentation for
        ``RegistrationProfile.send_acception_email()`` for information about
        these templates and the contexts provided to them.

        If ``REGISTRATION_ACCEPTION_EMAIL`` of settings is ``None``, no 
        acception email will be sent.

        After successful acception, the signal
        ``registration.signals.user_accepted`` will be sent, with the newly
        accepted ``User`` as the keyword argument ``uesr``, the ``RegistrationProfile``
        of the ``User`` as the keyword argument ``profile`` and the class of this
        backend as the sender

        """
        if send_email is None:
            send_email = settings.REGISTRATION_ACCEPTION_EMAIL

        accepted_user = RegistrationProfile.objects.accept_registration(
                profile, self.get_site(request),
                send_email=send_email, message=message)

        if accepted_user:
            signals.user_accepted.send(
                    sender=self.__class__,
                    user=accepted_user,
                    profile=profile,
                    request=request,
                )

        return accepted_user

    def reject(self, profile, request, send_email=None, message=None):
        """reject the account registration of ``profile``

        Given a profile, reject account registration, which will
        set inspection status of ``profile`` to ``rejected`` and delete 
        activation key of ``profile`` if exists.

        An email will be sent to the supplied email address; The email will be
        rendered using two templates. See the documentation for
        ``RegistrationProfile.send_rejection_email()`` for information about
        these templates and the contexts provided to them.

        If ``REGISTRATION_REJECTION_EMAIL`` of settings is ``None``, no 
        rejection email will be sent.

        After successful rejection, the signal
        ``registration.signals.user_rejected`` will be sent, with the newly
        rejected ``User`` as the keyword argument ``uesr``, the ``RegistrationProfile``
        of the ``User`` as the keyword argument ``profile`` and the class of this
        backend as the sender

        """
        if send_email is None:
            send_email = settings.REGISTRATION_REJECTION_EMAIL

        rejected_user = RegistrationProfile.objects.reject_registration(
                profile, self.get_site(request), 
                send_email=send_email, message=message)

        if rejected_user:
            signals.user_rejected.send(
                    sender=self.__class__,
                    user=rejected_user,
                    profile=profile,
                    request=request,
                )

        return rejected_user

    def activate(self, activation_key, request, password=None, send_email=None, 
            message=None, no_profile_delete=False):
        """activate user with ``activation_key`` and ``password``

        Given an activation key, password, look up and activate the user
        account corresponding to that key (if possible) and set its password.

        If ``password`` is not given, password will be generated

        An email will be sent to the supplied email address; The email will be
        rendered using two templates. See the documentation for
        ``RegistrationProfile.send_activation_email()`` for information about
        these templates and the contexts provided to them.

        If ``REGISTRATION_ACTIVATION_EMAIL`` of settings is ``None``, no 
        activation email will be sent.

        After successful activation, the signal
        ``registration.signals.user_activated`` will be sent, with the newly
        activated ``User`` as the keyword argument ``uesr``, the password
        of the ``User`` as the keyword argument ``password``, whether the password
        has generated or not as the keyword argument ``is_generated`` and the class
        of this backend as the sender

        """
        if send_email is None:
            send_email = settings.REGISTRATION_ACTIVATION_EMAIL

        activated = RegistrationProfile.objects.activate_user(
                activation_key=activation_key,
                site=self.get_site(request),
                password=password,
                send_email=send_email,
                message=message,
                no_profile_delete=no_profile_delete)

        if activated:
            user, password, is_generated = activated
            signals.user_activated.send(
                    sender=self.__class__,
                    user=user,
                    password=password,
                    is_generated=is_generated,
                    request=request,
                )
            return user
        return None

    def get_supplement_class(self):
        """Return the current registration supplement class"""
        # cache mechanisms will break the test thus disable it in test
        if not hasattr(self, '_supplement_class_cache') or 'test' in sys.argv:
            cls = get_supplement_class()
            setattr(self, '_supplement_class_cache', cls)
        return getattr(self, '_supplement_class_cache')

    def get_activation_form_class(self):
        """Return the default form class used for user activation"""
        return ActivationForm

    def get_registration_form_class(self):
        """Return the default form class used for user registration"""
        return RegistrationForm

    def get_supplement_form_class(self):
        """Return the default form class used for user registration supplement"""
        supplement_class = self.get_supplement_class()
        if not supplement_class:
            return None
        return supplement_class.get_form_class()
        
    def get_activation_complete_url(self, user):
        """Return a url to redirect to after successful user activation"""
        return reverse('registration_activation_complete')

    def get_registration_complete_url(self, user):
        """Return a url to redirect to after successful user registration"""
        return reverse('registration_complete')

    def get_registration_closed_url(self):
        """Return a url to redirect to if registration is closed"""
        return reverse('registration_disallowed')

    def registration_allowed(self):
        """
        Indicate whether account registration is currently permitted, based on
        the value of the setting ``REGISTRATION_OEPN``. This is determined as
        follows:

        *   If ``REGISTRATION_OPEN`` is not specified in settings, or is set
            to ``True``, registration is permitted.

        *   If ``REGISTRATION_OPEN`` is both specified and set to ``False``,
            registration is not permitted.

        """
        return getattr(settings, 'REGISTRATION_OPEN', True)
