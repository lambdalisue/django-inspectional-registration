#!/usr/bin/env python
# vim: set fileencoding=utf8:
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
from django.test import TestCase
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core import mail

from ..backends.default import DefaultRegistrationBackend
from ..models import RegistrationProfile
from ..admin import RegistrationAdmin

from override_settings import override_settings
from mock import mock_request


@override_settings(
        ACCOUNT_ACTIVATION_DAYS=7,
        REGISTRATION_OPEN=True,
        REGISTRATION_SUPPLEMENT_CLASS=None,
        REGISTRATION_BACKEND_CLASS='registration.backends.default.DefaultRegistrationBackend',
    )
class RegistrationAdminTestCase(TestCase):
    backend = DefaultRegistrationBackend()
    mock_request = mock_request()
    admin_url = reverse('admin:index')

    def setUp(self):
        self.admin = User.objects.create_superuser(
                username='mark', email='mark@test.com',
                password='password')

        self.client.login(username='mark', password='password')

    def test_change_list_view_get(self):
        url = self.admin_url + "registration/registrationprofile/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                'admin/change_list.html')

    def test_change_view_get(self):
        self.backend.register(
                username='bob', email='bob@example.com',
                request=self.mock_request)

        url = self.admin_url + "registration/registrationprofile/1/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                'admin/registration/registrationprofile/change_form.html')

    def test_change_view_get_404(self):
        self.backend.register(
                username='bob', email='bob@example.com',
                request=self.mock_request)

        url = self.admin_url + "registration/registrationprofile/100/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_change_view_post_valid_accept_from_untreated(self):
        new_user = self.backend.register(
                username='bob', email='bob@example.com',
                request=self.mock_request)

        url = self.admin_url + "registration/registrationprofile/1/"
        redirect_url = self.admin_url + "registration/registrationprofile/"
        response = self.client.post(url, {
                '_supplement-TOTAL_FORMS': 0, 
                '_supplement-INITIAL_FORMS': 0,
                '_supplement-MAXNUM_FORMS': '',
                'action': 'accept'
            })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

        profile = RegistrationProfile.objects.get(user__pk=new_user.pk)
        self.assertEqual(profile.status, 'accepted')

    def test_change_view_post_valid_inaccept_from_accepted(self):
        new_user = self.backend.register(
                username='bob', email='bob@example.com',
                request=self.mock_request)
        self.backend.accept(
                new_user.registration_profile,
                request=self.mock_request)

        url = self.admin_url + "registration/registrationprofile/1/"
        response = self.client.post(url, {
                '_supplement-TOTAL_FORMS': 0, 
                '_supplement-INITIAL_FORMS': 0,
                '_supplement-MAXNUM_FORMS': '',
                'action': 'accept'
            })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                'admin/registration/registrationprofile/change_form.html')
        self.failIf(response.context['adminform'].form.is_valid())
        self.assertEqual(
                response.context['adminform'].form.errors['action'],
                [u"Select a valid choice. accept is not one of the available choices."])

        profile = RegistrationProfile.objects.get(user__pk=new_user.pk)
        self.assertEqual(profile.status, 'accepted')

    def test_change_view_post_valid_accept_from_rejected(self):
        new_user = self.backend.register(
                username='bob', email='bob@example.com',
                request=self.mock_request)
        self.backend.reject(
                new_user.registration_profile,
                request=self.mock_request)

        url = self.admin_url + "registration/registrationprofile/1/"
        redirect_url = self.admin_url + "registration/registrationprofile/"
        response = self.client.post(url, {
                '_supplement-TOTAL_FORMS': 0, 
                '_supplement-INITIAL_FORMS': 0,
                '_supplement-MAXNUM_FORMS': '',
                'action': 'accept'
            })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

        profile = RegistrationProfile.objects.get(user__pk=new_user.pk)
        self.assertEqual(profile.status, 'accepted')

    def test_change_view_post_valid_reject_from_untreated(self):
        new_user = self.backend.register(
                username='bob', email='bob@example.com',
                request=self.mock_request)

        url = self.admin_url + "registration/registrationprofile/1/"
        redirect_url = self.admin_url + "registration/registrationprofile/"
        response = self.client.post(url, {
                '_supplement-TOTAL_FORMS': 0, 
                '_supplement-INITIAL_FORMS': 0,
                '_supplement-MAXNUM_FORMS': '',
                'action': 'reject'
            })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

        profile = RegistrationProfile.objects.get(user__pk=new_user.pk)
        self.assertEqual(profile.status, 'rejected')

    def test_change_view_post_invalid_reject_from_accepted(self):
        new_user = self.backend.register(
                username='bob', email='bob@example.com',
                request=self.mock_request)
        self.backend.accept(
                new_user.registration_profile,
                request=self.mock_request)

        url = self.admin_url + "registration/registrationprofile/1/"
        response = self.client.post(url, {
                '_supplement-TOTAL_FORMS': 0, 
                '_supplement-INITIAL_FORMS': 0,
                '_supplement-MAXNUM_FORMS': '',
                'action': 'reject'
            })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                'admin/registration/registrationprofile/change_form.html')
        self.failIf(response.context['adminform'].form.is_valid())
        self.assertEqual(
                response.context['adminform'].form.errors['action'],
                [u"Select a valid choice. reject is not one of the available choices."])

        profile = RegistrationProfile.objects.get(user__pk=new_user.pk)
        self.assertEqual(profile.status, 'accepted')

    def test_change_view_post_invalid_reject_from_rejected(self):
        new_user = self.backend.register(
                username='bob', email='bob@example.com',
                request=self.mock_request)
        self.backend.reject(
                new_user.registration_profile,
                request=self.mock_request)

        url = self.admin_url + "registration/registrationprofile/1/"
        response = self.client.post(url, {
                '_supplement-TOTAL_FORMS': 0, 
                '_supplement-INITIAL_FORMS': 0,
                '_supplement-MAXNUM_FORMS': '',
                'action': 'reject'
            })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                'admin/registration/registrationprofile/change_form.html')
        self.failIf(response.context['adminform'].form.is_valid())
        self.assertEqual(
                response.context['adminform'].form.errors['action'],
                [u"Select a valid choice. reject is not one of the available choices."])

        profile = RegistrationProfile.objects.get(user__pk=new_user.pk)
        self.assertEqual(profile.status, 'rejected')

    def test_change_view_post_invalid_activate_from_untreated(self):
        new_user = self.backend.register(
                username='bob', email='bob@example.com',
                request=self.mock_request)

        url = self.admin_url + "registration/registrationprofile/1/"
        response = self.client.post(url, {
                '_supplement-TOTAL_FORMS': 0, 
                '_supplement-INITIAL_FORMS': 0,
                '_supplement-MAXNUM_FORMS': '',
                'action': 'activate'
            })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                'admin/registration/registrationprofile/change_form.html')
        self.failIf(response.context['adminform'].form.is_valid())
        self.assertEqual(
                response.context['adminform'].form.errors['action'],
                [u"Select a valid choice. activate is not one of the available choices."])

        profile = RegistrationProfile.objects.get(user__pk=new_user.pk)
        self.assertEqual(profile.status, 'untreated')

    def test_change_view_post_valid_activate_from_accepted(self):
        new_user = self.backend.register(
                username='bob', email='bob@example.com',
                request=self.mock_request)
        self.backend.accept(
                new_user.registration_profile,
                request=self.mock_request)

        url = self.admin_url + "registration/registrationprofile/1/"
        redirect_url = self.admin_url + "registration/registrationprofile/"
        response = self.client.post(url, {
                '_supplement-TOTAL_FORMS': 0, 
                '_supplement-INITIAL_FORMS': 0,
                '_supplement-MAXNUM_FORMS': '',
                'action': 'activate'
            })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

        profile = RegistrationProfile.objects.filter(user__pk=new_user.pk)
        self.failIf(profile.exists())

    def test_change_view_post_invalid_activate_from_rejected(self):
        new_user = self.backend.register(
                username='bob', email='bob@example.com',
                request=self.mock_request)
        self.backend.reject(
                new_user.registration_profile,
                request=self.mock_request)

        url = self.admin_url + "registration/registrationprofile/1/"
        response = self.client.post(url, {
                '_supplement-TOTAL_FORMS': 0, 
                '_supplement-INITIAL_FORMS': 0,
                '_supplement-MAXNUM_FORMS': '',
                'action': 'activate'
            })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                'admin/registration/registrationprofile/change_form.html')
        self.failIf(response.context['adminform'].form.is_valid())
        self.assertEqual(
                response.context['adminform'].form.errors['action'],
                [u"Select a valid choice. activate is not one of the available choices."])

        profile = RegistrationProfile.objects.get(user__pk=new_user.pk)
        self.assertEqual(profile.status, 'rejected')

    def test_change_view_post_valid_force_activate_from_untreated(self):
        new_user = self.backend.register(
                username='bob', email='bob@example.com',
                request=self.mock_request)

        url = self.admin_url + "registration/registrationprofile/1/"
        redirect_url = self.admin_url + "registration/registrationprofile/"
        response = self.client.post(url, {
                '_supplement-TOTAL_FORMS': 0, 
                '_supplement-INITIAL_FORMS': 0,
                '_supplement-MAXNUM_FORMS': '',
                'action': 'force_activate'
            })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

        profile = RegistrationProfile.objects.filter(user__pk=new_user.pk)
        self.failIf(profile.exists())

    def test_change_view_post_invalid_force_activate_from_accepted(self):
        new_user = self.backend.register(
                username='bob', email='bob@example.com',
                request=self.mock_request)
        self.backend.accept(
                new_user.registration_profile,
                request=self.mock_request)

        url = self.admin_url + "registration/registrationprofile/1/"
        response = self.client.post(url, {
                '_supplement-TOTAL_FORMS': 0, 
                '_supplement-INITIAL_FORMS': 0,
                '_supplement-MAXNUM_FORMS': '',
                'action': 'force_activate'
            })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                'admin/registration/registrationprofile/change_form.html')
        self.failIf(response.context['adminform'].form.is_valid())
        self.assertEqual(
                response.context['adminform'].form.errors['action'],
                [u"Select a valid choice. force_activate is not one of the available choices."])

        profile = RegistrationProfile.objects.get(user__pk=new_user.pk)
        self.assertEqual(profile.status, 'accepted')

    def test_change_view_post_valid_force_activate_from_rejected(self):
        new_user = self.backend.register(
                username='bob', email='bob@example.com',
                request=self.mock_request)
        self.backend.reject(
                new_user.registration_profile,
                request=self.mock_request)

        url = self.admin_url + "registration/registrationprofile/1/"
        redirect_url = self.admin_url + "registration/registrationprofile/"
        response = self.client.post(url, {
                '_supplement-TOTAL_FORMS': 0, 
                '_supplement-INITIAL_FORMS': 0,
                '_supplement-MAXNUM_FORMS': '',
                'action': 'force_activate'
            })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

        profile = RegistrationProfile.objects.filter(user__pk=new_user.pk)
        self.failIf(profile.exists())

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
