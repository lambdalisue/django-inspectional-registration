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
from django.core.urlresolvers import reverse

from base import BackendBase
from .. import signals
from ..models import RegistrationProfile
from ..forms import ActivationForm
from ..forms import RegistrationForm

class DefaultBackend(BackendBase):

    def register(self, username, email):
        new_user = RegistrationProfile.objects.register(username, email)

        signals.user_registered.send(
                sender=self.__class__,
                user=new_user,
                profile=new_user.registration_profile
            )

        return new_user

    def accept(self, profile):

        accepted_user = RegistrationProfile.objects.accept_registration(profile)

        if accepted_user:
            signals.user_accepted.send(
                    sender=self.__class__,
                    user=accepted_user,
                    profile=profile
                )

        return accepted_user

    def reject(self, profile):

        rejected_user = RegistrationProfile.objects.reject_registration(profile)

        if rejected_user:
            signals.user_rejected.send(
                    sender=self.__class__,
                    user=rejected_user,
                    profile=profile,
                )

        return rejected_user

    def activate(self, activation_key, password=None):

        activated = RegistrationProfile.objects.activate_user(
                activation_key=activation_key,
                password=password)

        if activated:
            user, password, is_generated = activated
            signals.user_activated.send(
                    sender=self.__class__,
                    user=user,
                    password=password,
                    is_generated=is_generated,
                )
            return user
        return None

    def get_activation_form_class(self):
        return ActivationForm

    def get_registration_form_class(self):
        return RegistrationForm
        
    def get_activation_complete_url(self, user):
        return reverse('registration_activation_complete')

    def get_registration_complete_url(self, user):
        return reverse('registration_complete')

    def get_registration_closed_url(self):
        return reverse('registration_disallowed')

    def registration_allowed(self):
        return getattr(settings, 'REGISTRATION_OPEN', True)
