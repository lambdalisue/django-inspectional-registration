#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
"""
Unittest module of ...


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
import datetime
from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.contrib import admin
from django.contrib.auth.models import User

from .. import forms
from .. import signals
from ..backends import get_backend
from ..backends.default import DefaultRegistrationBackend
from ..models import RegistrationProfile
from ..admin import RegistrationAdmin

from base import RegistrationTestCaseBase

class RegistrationBackendRetrievalTests(RegistrationTestCaseBase):

    def test_get_backend(self):
        backend = get_backend('registration.backends.default.DefaultRegistrationBackend')
        self.failUnless(isinstance(backend, DefaultRegistrationBackend))

    def test_backend_error_invalid(self):
        self.assertRaises(ImproperlyConfigured, get_backend,
                'registration.backends.doesnotexist.NonExistenBackend')

    def test_backend_attribute_error(self):
        self.assertRaises(ImproperlyConfigured, get_backend,
                'registration.backends.default.NonexistenBackend')

class DefaultRegistrationBackendTestCase(RegistrationTestCaseBase):

    def test_registration(self):
        new_user = self.backend.register(
                username='bob', email='bob@example.com',
                request=self.mock_request)

        self.assertEqual(new_user.username, 'bob')
        self.assertEqual(new_user.email, 'bob@example.com')

        self.failIf(new_user.is_active)
        self.failIf(new_user.has_usable_password())

        # A inspection profile was created, and an registration email
        # was sent.
        self.assertEqual(RegistrationProfile.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_acceptance(self):
        new_user = self.backend.register(
                username='bob', email='bob@example.com',
                request=self.mock_request)

        profile = new_user.registration_profile
        accepted_user = self.backend.accept(profile, request=self.mock_request)

        self.failUnless(accepted_user)
        self.assertEqual(profile, accepted_user.registration_profile)
        self.assertEqual(profile.status, 'accepted')
        self.assertNotEqual(profile.activation_key, None)

    def test_rejection(self):
        new_user = self.backend.register(
                username='bob', email='bob@example.com',
                request=self.mock_request)

        profile = new_user.registration_profile
        rejected_user = self.backend.reject(profile, request=self.mock_request)

        self.failUnless(rejected_user)
        self.assertEqual(profile, rejected_user.registration_profile)
        self.assertEqual(profile.status, 'rejected')
        self.assertEqual(profile.activation_key, None)

    def test_activation_with_password(self):
        new_user = self.backend.register(
                username='bob', email='bob@example.com',
                request=self.mock_request)

        profile = new_user.registration_profile
        self.backend.accept(profile, request=self.mock_request)
        activated_user = self.backend.activate(
                activation_key=profile.activation_key,
                request=self.mock_request,
                password='swardfish')

        self.failUnless(activated_user)
        self.assertEqual(activated_user, new_user)
        self.failUnless(activated_user.is_active)
        self.failUnless(activated_user.has_usable_password())
        self.failUnless(activated_user.check_password('swardfish'))

    def test_activation_without_password(self):
        new_user = self.backend.register(
                username='bob', email='bob@example.com',
                request=self.mock_request)

        profile = new_user.registration_profile
        self.backend.accept(profile, request=self.mock_request)
        activated_user = self.backend.activate(
                activation_key=profile.activation_key,
                request=self.mock_request)

        self.failUnless(activated_user)
        self.assertEqual(activated_user, new_user)
        self.failUnless(activated_user.is_active)
        self.failUnless(activated_user.has_usable_password())

    def test_untreated_activation(self):
        new_user = self.backend.register(
                username='bob', email='bob@example.com',
                request=self.mock_request)

        profile = new_user.registration_profile
        activated_user = self.backend.activate(
                activation_key=profile.activation_key,
                request=self.mock_request,
                password='swardfish')

        self.failIf(activated_user)
        new_user = User.objects.get(pk=new_user.pk)
        self.failIf(new_user.is_active)
        self.failIf(new_user.has_usable_password())

    def test_rejected_activation(self):
        new_user = self.backend.register(
                username='bob', email='bob@example.com',
                request=self.mock_request)

        profile = new_user.registration_profile
        self.backend.reject(profile, request=self.mock_request)
        activated_user = self.backend.activate(
                activation_key=profile.activation_key,
                request=self.mock_request,
                password='swardfish')

        self.failIf(activated_user)
        new_user = User.objects.get(pk=new_user.pk)
        self.failIf(new_user.is_active)
        self.failIf(new_user.has_usable_password())

    def test_expired_activation(self):
        expired_user = self.backend.register(
                username='bob', email='bob@example.com',
                request=self.mock_request)

        profile = expired_user.registration_profile
        self.backend.accept(profile, request=self.mock_request)

        expired_user.date_joined -= datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS+1)
        expired_user.save()

        activated_user = self.backend.activate(
                activation_key=profile.activation_key,
                request=self.mock_request,
                password='swardfish')

        self.failIf(activated_user)
        expired_user = User.objects.get(pk=expired_user.pk)
        self.failIf(expired_user.is_active)
        self.failIf(expired_user.has_usable_password())

    def test_allow(self):
        old_allowed = settings.REGISTRATION_OPEN
        settings.REGISTRATION_OPEN = True
        self.failUnless(self.backend.registration_allowed())

        settings.REGISTRATION_OPEN = False
        self.failIf(self.backend.registration_allowed())
        settings.REGISTRATION_OPEN = old_allowed

    def test_get_registration_form_class(self):
        form_class = self.backend.get_registration_form_class()
        self.failUnless(form_class is forms.RegistrationForm)

    def test_get_activation_form_class(self):
        form_class = self.backend.get_activation_form_class()
        self.failUnless(form_class is forms.ActivationForm)

    def test_get_registration_complete_url(self):
        fake_user = User()
        url = self.backend.get_registration_complete_url(fake_user)
        self.assertEqual(url, reverse('registration_complete'))

    def test_get_registration_closed_url(self):
        url = self.backend.get_registration_closed_url()
        self.assertEqual(url, reverse('registration_disallowed'))

    def test_get_activation_complete_url(self):
        fake_user = User()
        url = self.backend.get_activation_complete_url(fake_user)
        self.assertEqual(url, reverse('registration_activation_complete'))

    def test_registration_signal(self):
        def receiver(sender, user, profile, **kwargs):
            self.assertEqual(user.username, 'bob')
            self.assertEqual(user.registration_profile, profile)
            received_signals.append(kwargs.get('signal'))

        received_signals = []
        signals.user_registered.connect(receiver, sender=self.backend.__class__)

        self.backend.register(username='bob', email='bob@example.com', request=self.mock_request)

        self.assertEqual(len(received_signals), 1)
        self.assertEqual(received_signals, [signals.user_registered])

    def test_acceptance_signal(self):
        def receiver(sender, user, profile, **kwargs):
            self.assertEqual(user.username, 'bob')
            self.assertEqual(user.registration_profile, profile)
            received_signals.append(kwargs.get('signal'))

        received_signals = []
        signals.user_accepted.connect(receiver, sender=self.backend.__class__)

        self.backend.register(username='bob', email='bob@example.com', request=self.mock_request)
        profile = RegistrationProfile.objects.get(user__username='bob')
        self.backend.accept(profile, request=self.mock_request)

        self.assertEqual(len(received_signals), 1)
        self.assertEqual(received_signals, [signals.user_accepted])

    def test_acceptance_signal_fail(self):
        def receiver(sender, user, profile, **kwargs):
            self.assertEqual(user.username, 'bob')
            self.assertEqual(user.registration_profile, profile)
            received_signals.append(kwargs.get('signal'))

        received_signals = []

        self.backend.register(username='bob', email='bob@example.com', request=self.mock_request)
        profile = RegistrationProfile.objects.get(user__username='bob')
        self.backend.accept(profile, request=self.mock_request)

        signals.user_accepted.connect(receiver, sender=self.backend.__class__)
        # accept -> accept is not allowed thus fail
        self.backend.accept(profile, request=self.mock_request)

        self.assertEqual(len(received_signals), 0)

    def test_rejection_signal(self):
        def receiver(sender, user, profile, **kwargs):
            self.assertEqual(user.username, 'bob')
            self.assertEqual(user.registration_profile, profile)
            received_signals.append(kwargs.get('signal'))

        received_signals = []
        signals.user_rejected.connect(receiver, sender=self.backend.__class__)

        self.backend.register(username='bob', email='bob@example.com', request=self.mock_request)
        profile = RegistrationProfile.objects.get(user__username='bob')
        self.backend.reject(profile, request=self.mock_request)

        self.assertEqual(len(received_signals), 1)
        self.assertEqual(received_signals, [signals.user_rejected])

    def test_rejection_signal_fail(self):
        def receiver(sender, user, profile, **kwargs):
            self.assertEqual(user.username, 'bob')
            self.assertEqual(user.registration_profile, profile)
            received_signals.append(kwargs.get('signal'))

        received_signals = []
        signals.user_rejected.connect(receiver, sender=self.backend.__class__)

        self.backend.register(username='bob', email='bob@example.com', request=self.mock_request)
        profile = RegistrationProfile.objects.get(user__username='bob')
        self.backend.accept(profile, request=self.mock_request)
        # accept -> reject is not allowed
        self.backend.reject(profile, request=self.mock_request)

        self.assertEqual(len(received_signals), 0)

    def test_activation_signal(self):
        def receiver(sender, user, password, is_generated, **kwargs):
            self.assertEqual(user.username, 'bob')
            self.assertEqual(password, 'swordfish')
            self.failIf(is_generated)
            received_signals.append(kwargs.get('signal'))

        received_signals = []
        signals.user_activated.connect(receiver, sender=self.backend.__class__)

        self.backend.register(username='bob', email='bob@example.com', request=self.mock_request)
        profile = RegistrationProfile.objects.get(user__username='bob')
        self.backend.accept(profile, request=self.mock_request)
        self.backend.activate(profile.activation_key, request=self.mock_request, password='swordfish')

        self.assertEqual(len(received_signals), 1)
        self.assertEqual(received_signals, [signals.user_activated])

class RegistrationAdminTestCase(RegistrationTestCaseBase):

    def test_resend_acceptance_email_action(self):
        admin_class = RegistrationAdmin(RegistrationProfile, admin.site)

        self.backend.register(username='bob', email='bob@example.com', request=self.mock_request)
        admin_class.resend_acceptance_email(None, RegistrationProfile.objects.all())

        # one for registration, one for resend
        self.assertEqual(len(mail.outbox), 2)

    def test_accept_users_action(self):
        admin_class = RegistrationAdmin(RegistrationProfile, admin.site)

        self.backend.register(username='bob', email='bob@example.com', request=self.mock_request)
        admin_class.accept_users(None, RegistrationProfile.objects.all())

        for profile in RegistrationProfile.objects.all():
            self.assertEqual(profile.status, 'accepted')
            self.assertNotEqual(profile.activation_key, None)

    def test_reject_users_action(self):
        admin_class = RegistrationAdmin(RegistrationProfile, admin.site)

        self.backend.register(username='bob', email='bob@example.com', request=self.mock_request)
        admin_class.reject_users(None, RegistrationProfile.objects.all())

        for profile in RegistrationProfile.objects.all():
            self.assertEqual(profile.status, 'rejected')
            self.assertEqual(profile.activation_key, None)

    def test_force_activate_users_action(self):
        admin_class = RegistrationAdmin(RegistrationProfile, admin.site)

        self.backend.register(username='bob', email='bob@example.com', request=self.mock_request)
        admin_class.force_activate_users(None, RegistrationProfile.objects.all())

        self.assertEqual(RegistrationProfile.objects.count(), 0)
