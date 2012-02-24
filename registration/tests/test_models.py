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
import datetime

from django.conf import settings
from django.core import mail
from django.core import management
from django.test import TestCase
from django.contrib.auth.models import User

from ..models import RegistrationProfile

from base import RegistrationTestCaseBase

class RegistrationProfileTestCase(RegistrationTestCaseBase):
    user_info = {
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'password'
        }

    def create_inactive_user(self):
        new_user = User.objects.create_user(**self.user_info)
        new_user.set_unusable_password()
        new_user.is_active = False
        return new_user

    def test_profile_creation(self):
        new_user = self.create_inactive_user()
        profile = RegistrationProfile.objects.create(user=new_user)

        self.assertEqual(RegistrationProfile.objects.count(), 1)
        self.assertEqual(profile.user.id, new_user.id)
        self.assertEqual(profile.status, 'untreated')
        self.assertEqual(profile.activation_key, None)
        self.assertEqual(unicode(profile), "Registration information for alice")

    def test_profile_status_modification(self):
        new_user = self.create_inactive_user()
        profile = RegistrationProfile.objects.create(user=new_user)

        profile.status = 'accepted'
        self.assertEqual(profile.status, 'accepted')
        self.assertNotEqual(profile.activation_key, None)
        self.assertEqual(profile.activation_key_expired(), False)

        profile.status = 'rejected'
        self.assertEqual(profile.status, 'rejected')
        self.assertEqual(profile.activation_key, None)
        self.assertEqual(profile.activation_key_expired(), False)

        profile.status = 'accepted'
        self.assertEqual(profile.status, 'accepted')
        self.assertNotEqual(profile.activation_key, None)
        self.assertEqual(profile.activation_key_expired(), False)

        profile.status = 'untreated'
        self.assertEqual(profile.status, 'untreated')
        self.assertEqual(profile.activation_key, None)
        self.assertEqual(profile.activation_key_expired(), False)

        new_user.date_joined -= datetime.timedelta(settings.ACCOUNT_ACTIVATION_DAYS+1)
        profile.status = 'untreated'
        self.assertEqual(profile.status, 'untreated')
        self.assertEqual(profile.activation_key_expired(), False)
        profile.status = 'rejected'
        self.assertEqual(profile.status, 'rejected')
        self.assertEqual(profile.activation_key_expired(), False)
        profile.status = 'accepted'
        # status = accepted change date_joined
        new_user.date_joined -= datetime.timedelta(settings.ACCOUNT_ACTIVATION_DAYS+1)
        self.assertEqual(profile.status, 'expired')
        self.assertEqual(profile.activation_key_expired(), True)

    def test_send_registration_email(self):
        new_user = self.create_inactive_user()
        profile = RegistrationProfile.objects.create(user=new_user)
        profile.send_registration_email()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user_info['email']])

    def test_send_activation_email(self):
        new_user = self.create_inactive_user()
        profile = RegistrationProfile.objects.create(user=new_user)
        profile.send_activation_email()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user_info['email']])

    def test_send_acception_email(self):
        new_user = self.create_inactive_user()
        profile = RegistrationProfile.objects.create(user=new_user)
        profile.send_acception_email()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user_info['email']])

    def test_send_rejection_email(self):
        new_user = self.create_inactive_user()
        profile = RegistrationProfile.objects.create(user=new_user)
        profile.status = 'rejected'
        profile.save()
        profile.send_rejection_email()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user_info['email']])

class RegistrationProfileManagerTestCase(RegistrationTestCaseBase):
    user_info = {
            'username': 'alice',
            'email': 'alice@example.com',
        }

    def test_register(self):
        new_user = RegistrationProfile.objects.register(**self.user_info)
        self.assertEqual(new_user.username, 'alice')
        self.assertEqual(new_user.email, 'alice@example.com')
        self.failIf(new_user.is_active)
        self.failIf(new_user.has_usable_password())

    def test_register_email(self):
        RegistrationProfile.objects.register(**self.user_info)

        self.assertEqual(len(mail.outbox), 1)

    def test_register_no_email(self):
        RegistrationProfile.objects.register(send_email=False, **self.user_info)

        self.assertEqual(len(mail.outbox), 0)

    def test_acception(self):
        new_user = RegistrationProfile.objects.register(
                send_email=False, **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.accept_registration(profile)

        self.assertEqual(profile.status, 'accepted')
        self.assertNotEqual(profile.activation_key, None)

    def test_acception_email(self):
        new_user = RegistrationProfile.objects.register(
                send_email=False, **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.accept_registration(profile)

        self.assertEqual(len(mail.outbox), 1)

    def test_acception_no_email(self):
        new_user = RegistrationProfile.objects.register(
                send_email=False, **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.accept_registration(profile, send_email=False)

        self.assertEqual(len(mail.outbox), 0)

    def test_rejection(self):
        new_user = RegistrationProfile.objects.register(
                send_email=False, **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.reject_registration(profile)

        self.assertEqual(profile.status, 'rejected')
        self.assertEqual(profile.activation_key, None)

    def test_rejection_email(self):
        new_user = RegistrationProfile.objects.register(
                send_email=False, **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.reject_registration(profile)

        self.assertEqual(len(mail.outbox), 1)

    def test_rejection_no_email(self):
        new_user = RegistrationProfile.objects.register(
                send_email=False, **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.reject_registration(profile, send_email=False)

        self.assertEqual(len(mail.outbox), 0)

    def test_acception_after_rejection_success(self):
        new_user = RegistrationProfile.objects.register(
                send_email=False, **self.user_info)

        profile = new_user.registration_profile

        # reject
        result = RegistrationProfile.objects.reject_registration(profile)
        self.failUnless(result)
        self.assertEqual(profile.status, 'rejected')
        self.assertEqual(profile.activation_key, None)

        # accept should work even after rejection
        result = RegistrationProfile.objects.accept_registration(profile)
        self.failUnless(result)
        self.assertEqual(profile.status, 'accepted')
        self.assertNotEqual(profile.activation_key, None)

    def test_acception_after_acception_fail(self):
        new_user = RegistrationProfile.objects.register(
                send_email=False, **self.user_info)

        profile = new_user.registration_profile

        # accept
        result = RegistrationProfile.objects.accept_registration(profile)
        self.failUnless(result)
        self.assertEqual(profile.status, 'accepted')
        self.assertNotEqual(profile.activation_key, None)

        # accept should not work
        result = RegistrationProfile.objects.accept_registration(profile)
        self.failIf(result)
        self.assertEqual(profile.status, 'accepted')
        self.assertNotEqual(profile.activation_key, None)

    def test_rejection_after_acception_fail(self):
        new_user = RegistrationProfile.objects.register(
                send_email=False, **self.user_info)

        profile = new_user.registration_profile

        # accept
        result = RegistrationProfile.objects.accept_registration(profile)
        self.failUnless(result)
        self.assertEqual(profile.status, 'accepted')
        self.assertNotEqual(profile.activation_key, None)

        # reject should not work
        result = RegistrationProfile.objects.reject_registration(profile)
        self.failIf(result)
        self.assertEqual(profile.status, 'accepted')
        self.assertNotEqual(profile.activation_key, None)

    def test_rejection_after_rejection_fail(self):
        new_user = RegistrationProfile.objects.register(
                send_email=False, **self.user_info)

        profile = new_user.registration_profile

        # accept
        result = RegistrationProfile.objects.reject_registration(profile)
        self.failUnless(result)
        self.assertEqual(profile.status, 'rejected')
        self.assertEqual(profile.activation_key, None)

        # reject should not work
        result = RegistrationProfile.objects.reject_registration(profile)
        self.failIf(result)
        self.assertEqual(profile.status, 'rejected')
        self.assertEqual(profile.activation_key, None)

    def test_activation_with_password(self):
        new_user = RegistrationProfile.objects.register(
                send_email=False, **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.accept_registration(profile, send_email=False)
        activated = RegistrationProfile.objects.activate_user(
                activation_key=profile.activation_key,
                password='swordfish',
                send_email=False)

        self.failUnless(activated)

        activated_user, password, is_generated = activated

        self.assertEqual(new_user, activated_user)
        self.assertEqual(password, 'swordfish')
        self.assertEqual(is_generated, False)
        # the user should be activated with the password
        self.failUnless(activated_user.is_active)
        self.failUnless(activated_user.has_usable_password())
        self.failUnless(activated_user.check_password(password))
        # inspection profile should be deleted
        self.failIf(RegistrationProfile.objects.filter(pk=profile.pk).exists())

    def test_activation_without_password(self):
        new_user = RegistrationProfile.objects.register(
                send_email=False, **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.accept_registration(profile, send_email=False)
        activated = RegistrationProfile.objects.activate_user(
                activation_key=profile.activation_key,
                send_email=False)

        self.failUnless(activated)

        activated_user, password, is_generated = activated

        self.assertEqual(new_user, activated_user)
        self.assertEqual(len(password), settings.REGISTRATION_DEFAULT_PASSWORD_LENGTH)
        self.assertEqual(is_generated, True)
        # the user should be activated with the password
        self.failUnless(activated_user.is_active)
        self.failUnless(activated_user.has_usable_password())
        self.failUnless(activated_user.check_password(password))
        # inspection profile should be deleted
        self.failIf(RegistrationProfile.objects.filter(pk=profile.pk).exists())

    def test_activation_email(self):
        new_user = RegistrationProfile.objects.register(
                send_email=False, **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.accept_registration(profile, send_email=False)
        RegistrationProfile.objects.activate_user(
                activation_key=profile.activation_key)

        self.assertEqual(len(mail.outbox), 1)

    def test_activation_no_email(self):
        new_user = RegistrationProfile.objects.register(
                send_email=False, **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.accept_registration(profile, send_email=False)
        RegistrationProfile.objects.activate_user(
                activation_key=profile.activation_key,
                send_email=False)

        self.assertEqual(len(mail.outbox), 0)

    def test_activation_with_untreated_fail(self):
        new_user = RegistrationProfile.objects.register(
                send_email=False, **self.user_info)

        profile = new_user.registration_profile

        result = RegistrationProfile.objects.activate_user(
                activation_key=profile.activation_key,
                password='swordfish')

        self.failIf(result)
        # the user should not be activated
        self.failIf(new_user.is_active)
        self.failIf(new_user.has_usable_password())
        self.failIf(new_user.check_password('swordfish'))
        # inspection profile should not be deleted
        self.failUnless(RegistrationProfile.objects.filter(pk=profile.pk).exists())

    def test_activation_with_rejected_fail(self):
        new_user = RegistrationProfile.objects.register(
                send_email=False, **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.reject_registration(profile)

        result = RegistrationProfile.objects.activate_user(
                activation_key=profile.activation_key,
                password='swordfish')

        self.failIf(result)
        # the user should not be activated
        self.failIf(new_user.is_active)
        self.failIf(new_user.has_usable_password())
        self.failIf(new_user.check_password('swordfish'))
        # inspection profile should not be deleted
        self.failUnless(RegistrationProfile.objects.filter(pk=profile.pk).exists())

    def test_activation_with_expired_fail(self):
        new_user = RegistrationProfile.objects.register(
                send_email=False, **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.accept_registration(profile)

        new_user.date_joined -= datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS + 1)
        new_user.save()

        result = RegistrationProfile.objects.activate_user(
                activation_key=profile.activation_key,
                password='swordfish')

        self.failIf(result)
        # the user should not be activated
        self.failIf(new_user.is_active)
        self.failIf(new_user.has_usable_password())
        self.failIf(new_user.check_password('swordfish'))
        # inspection profile should not be deleted
        self.failUnless(RegistrationProfile.objects.filter(pk=profile.pk).exists())

    def test_activation_with_invalid_key_fail(self):
        new_user = RegistrationProfile.objects.register(
                send_email=False, **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.accept_registration(profile)

        result = RegistrationProfile.objects.activate_user(
                activation_key='foo',
                password='swordfish')

        self.failIf(result)
        # the user should not be activated
        self.failIf(new_user.is_active)
        self.failIf(new_user.has_usable_password())
        self.failIf(new_user.check_password('swordfish'))
        # inspection profile should not be deleted
        self.failUnless(RegistrationProfile.objects.filter(pk=profile.pk).exists())

    def test_expired_user_deletion(self):
        RegistrationProfile.objects.register(
                username='new untreated user',
                email='new_untreated_user@example.com')
        new_accepted_user = RegistrationProfile.objects.register(
                username='new accepted user',
                email='new_accepted_user@example.com')
        new_rejected_user = RegistrationProfile.objects.register(
                username='new rejected user',
                email='new_rejected_user@example.com')
        expired_untreated_user = RegistrationProfile.objects.register(
                username='expired untreated user',
                email='expired_untreated_user@example.com')
        expired_accepted_user = RegistrationProfile.objects.register(
                username='expired accepted user',
                email='expired_accepted_user@example.com')
        expired_rejected_user = RegistrationProfile.objects.register(
                username='expired rejected user',
                email='expired_rejected_user@example.com')

        RegistrationProfile.objects.accept_registration(
                new_accepted_user.registration_profile)
        RegistrationProfile.objects.reject_registration(
                new_rejected_user.registration_profile)
        RegistrationProfile.objects.accept_registration(
                expired_accepted_user.registration_profile)
        RegistrationProfile.objects.reject_registration(
                expired_rejected_user.registration_profile)

        delta = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS+1)

        expired_untreated_user.date_joined -= delta
        expired_untreated_user.save()
        expired_accepted_user.date_joined -= delta
        expired_accepted_user.save()
        expired_rejected_user.date_joined -= delta
        expired_rejected_user.save()

        RegistrationProfile.objects.delete_expired_users()
        # Only expired accepted user is deleted
        self.assertEqual(RegistrationProfile.objects.count(), 5)
        self.assertRaises(User.DoesNotExist, User.objects.get, 
                          username='expired accepted user')

    def test_rejected_user_deletion(self):
        RegistrationProfile.objects.register(
                username='new untreated user',
                email='new_untreated_user@example.com')
        new_accepted_user = RegistrationProfile.objects.register(
                username='new accepted user',
                email='new_accepted_user@example.com')
        new_rejected_user = RegistrationProfile.objects.register(
                username='new rejected user',
                email='new_rejected_user@example.com')
        expired_untreated_user = RegistrationProfile.objects.register(
                username='expired untreated user',
                email='expired_untreated_user@example.com')
        expired_accepted_user = RegistrationProfile.objects.register(
                username='expired accepted user',
                email='expired_accepted_user@example.com')
        expired_rejected_user = RegistrationProfile.objects.register(
                username='expired rejected user',
                email='expired_rejected_user@example.com')

        RegistrationProfile.objects.accept_registration(
                new_accepted_user.registration_profile)
        RegistrationProfile.objects.reject_registration(
                new_rejected_user.registration_profile)
        RegistrationProfile.objects.accept_registration(
                expired_accepted_user.registration_profile)
        RegistrationProfile.objects.reject_registration(
                expired_rejected_user.registration_profile)

        delta = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS+1)

        expired_untreated_user.date_joined -= delta
        expired_untreated_user.save()
        expired_accepted_user.date_joined -= delta
        expired_accepted_user.save()
        expired_rejected_user.date_joined -= delta
        expired_rejected_user.save()

        RegistrationProfile.objects.delete_rejected_users()
        # new_rejected_user and expired rejected user are deleted
        self.assertEqual(RegistrationProfile.objects.count(), 4)
        self.assertRaises(User.DoesNotExist, User.objects.get, 
                          username='new rejected user')
        self.assertRaises(User.DoesNotExist, User.objects.get, 
                          username='expired rejected user')

    def test_management_command_cleanup_expired_registrations(self):
        RegistrationProfile.objects.register(
                username='new untreated user',
                email='new_untreated_user@example.com')
        new_accepted_user = RegistrationProfile.objects.register(
                username='new accepted user',
                email='new_accepted_user@example.com')
        new_rejected_user = RegistrationProfile.objects.register(
                username='new rejected user',
                email='new_rejected_user@example.com')
        expired_untreated_user = RegistrationProfile.objects.register(
                username='expired untreated user',
                email='expired_untreated_user@example.com')
        expired_accepted_user = RegistrationProfile.objects.register(
                username='expired accepted user',
                email='expired_accepted_user@example.com')
        expired_rejected_user = RegistrationProfile.objects.register(
                username='expired rejected user',
                email='expired_rejected_user@example.com')

        RegistrationProfile.objects.accept_registration(
                new_accepted_user.registration_profile)
        RegistrationProfile.objects.reject_registration(
                new_rejected_user.registration_profile)
        RegistrationProfile.objects.accept_registration(
                expired_accepted_user.registration_profile)
        RegistrationProfile.objects.reject_registration(
                expired_rejected_user.registration_profile)

        delta = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS+1)

        expired_untreated_user.date_joined -= delta
        expired_untreated_user.save()
        expired_accepted_user.date_joined -= delta
        expired_accepted_user.save()
        expired_rejected_user.date_joined -= delta
        expired_rejected_user.save()

        management.call_command('cleanup_expired_registrations')
        # Only expired accepted user is deleted
        self.assertEqual(RegistrationProfile.objects.count(), 5)
        self.assertRaises(User.DoesNotExist, User.objects.get, 
                          username='expired accepted user')

    def test_management_command_cleanup_rejected_registrations(self):
        RegistrationProfile.objects.register(
                username='new untreated user',
                email='new_untreated_user@example.com')
        new_accepted_user = RegistrationProfile.objects.register(
                username='new accepted user',
                email='new_accepted_user@example.com')
        new_rejected_user = RegistrationProfile.objects.register(
                username='new rejected user',
                email='new_rejected_user@example.com')
        expired_untreated_user = RegistrationProfile.objects.register(
                username='expired untreated user',
                email='expired_untreated_user@example.com')
        expired_accepted_user = RegistrationProfile.objects.register(
                username='expired accepted user',
                email='expired_accepted_user@example.com')
        expired_rejected_user = RegistrationProfile.objects.register(
                username='expired rejected user',
                email='expired_rejected_user@example.com')

        RegistrationProfile.objects.accept_registration(
                new_accepted_user.registration_profile)
        RegistrationProfile.objects.reject_registration(
                new_rejected_user.registration_profile)
        RegistrationProfile.objects.accept_registration(
                expired_accepted_user.registration_profile)
        RegistrationProfile.objects.reject_registration(
                expired_rejected_user.registration_profile)

        delta = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS+1)

        expired_untreated_user.date_joined -= delta
        expired_untreated_user.save()
        expired_accepted_user.date_joined -= delta
        expired_accepted_user.save()
        expired_rejected_user.date_joined -= delta
        expired_rejected_user.save()

        management.call_command('cleanup_rejected_registrations')
        # new_rejected_user and expired rejected user are deleted
        self.assertEqual(RegistrationProfile.objects.count(), 4)
        self.assertRaises(User.DoesNotExist, User.objects.get, 
                          username='new rejected user')
        self.assertRaises(User.DoesNotExist, User.objects.get, 
                          username='expired rejected user')

    def test_management_command_cleanup_registrations(self):
        RegistrationProfile.objects.register(
                username='new untreated user',
                email='new_untreated_user@example.com')
        new_accepted_user = RegistrationProfile.objects.register(
                username='new accepted user',
                email='new_accepted_user@example.com')
        new_rejected_user = RegistrationProfile.objects.register(
                username='new rejected user',
                email='new_rejected_user@example.com')
        expired_untreated_user = RegistrationProfile.objects.register(
                username='expired untreated user',
                email='expired_untreated_user@example.com')
        expired_accepted_user = RegistrationProfile.objects.register(
                username='expired accepted user',
                email='expired_accepted_user@example.com')
        expired_rejected_user = RegistrationProfile.objects.register(
                username='expired rejected user',
                email='expired_rejected_user@example.com')

        RegistrationProfile.objects.accept_registration(
                new_accepted_user.registration_profile)
        RegistrationProfile.objects.reject_registration(
                new_rejected_user.registration_profile)
        RegistrationProfile.objects.accept_registration(
                expired_accepted_user.registration_profile)
        RegistrationProfile.objects.reject_registration(
                expired_rejected_user.registration_profile)

        delta = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS+1)

        expired_untreated_user.date_joined -= delta
        expired_untreated_user.save()
        expired_accepted_user.date_joined -= delta
        expired_accepted_user.save()
        expired_rejected_user.date_joined -= delta
        expired_rejected_user.save()

        management.call_command('cleanup_registrations')
        # new_rejected_user, expired rejected_user and expired_accepted_user are deleted
        self.assertEqual(RegistrationProfile.objects.count(), 3)
        self.assertRaises(User.DoesNotExist, User.objects.get, 
                          username='new rejected user')
        self.assertRaises(User.DoesNotExist, User.objects.get, 
                          username='expired rejected user')
        self.assertRaises(User.DoesNotExist, User.objects.get, 
                          username='expired accepted user')

    def test_management_command_cleanupregistration(self):
        RegistrationProfile.objects.register(
                username='new untreated user',
                email='new_untreated_user@example.com')
        new_accepted_user = RegistrationProfile.objects.register(
                username='new accepted user',
                email='new_accepted_user@example.com')
        new_rejected_user = RegistrationProfile.objects.register(
                username='new rejected user',
                email='new_rejected_user@example.com')
        expired_untreated_user = RegistrationProfile.objects.register(
                username='expired untreated user',
                email='expired_untreated_user@example.com')
        expired_accepted_user = RegistrationProfile.objects.register(
                username='expired accepted user',
                email='expired_accepted_user@example.com')
        expired_rejected_user = RegistrationProfile.objects.register(
                username='expired rejected user',
                email='expired_rejected_user@example.com')

        RegistrationProfile.objects.accept_registration(
                new_accepted_user.registration_profile)
        RegistrationProfile.objects.reject_registration(
                new_rejected_user.registration_profile)
        RegistrationProfile.objects.accept_registration(
                expired_accepted_user.registration_profile)
        RegistrationProfile.objects.reject_registration(
                expired_rejected_user.registration_profile)

        delta = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS+1)

        expired_untreated_user.date_joined -= delta
        expired_untreated_user.save()
        expired_accepted_user.date_joined -= delta
        expired_accepted_user.save()
        expired_rejected_user.date_joined -= delta
        expired_rejected_user.save()

        # django-registration compatibility
        management.call_command('cleanupregistration')
        # new_rejected_user, expired rejected_user and expired_accepted_user are deleted
        self.assertEqual(RegistrationProfile.objects.count(), 3)
        self.assertRaises(User.DoesNotExist, User.objects.get, 
                          username='new rejected user')
        self.assertRaises(User.DoesNotExist, User.objects.get, 
                          username='expired rejected user')
        self.assertRaises(User.DoesNotExist, User.objects.get, 
                          username='expired accepted user')
