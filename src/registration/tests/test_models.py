# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import datetime
from django.test import TestCase
from django.conf import settings
from django.core import mail
from django.core import management

from registration.compat import get_user_model
from registration.models import RegistrationProfile
from registration.utils import generate_activation_key
from registration.tests.mock import mock_site
from registration.tests.compat import override_settings


@override_settings(
    ACCOUNT_ACTIVATION_DAYS=7,
    REGISTRATION_OPEN=True,
    REGISTRATION_SUPPLEMENT_CLASS=None,
    REGISTRATION_BACKEND_CLASS=(
        'registration.backends.default.DefaultRegistrationBackend'),
)
class RegistrationProfileTestCase(TestCase):
    user_info = {
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'password'
    }

    def setUp(self):
        self.mock_site = mock_site()

    def create_inactive_user(self):
        User = get_user_model()
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
        self.assertEqual(unicode(profile),
                         "Registration information for alice")

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

        new_user.date_joined -= datetime.timedelta(
            settings.ACCOUNT_ACTIVATION_DAYS+1
        )
        profile.status = 'untreated'
        self.assertEqual(profile.status, 'untreated')
        self.assertEqual(profile.activation_key_expired(), False)
        profile.status = 'rejected'
        self.assertEqual(profile.status, 'rejected')
        self.assertEqual(profile.activation_key_expired(), False)
        profile.status = 'accepted'
        # status = accepted change date_joined
        new_user.date_joined -= datetime.timedelta(
            settings.ACCOUNT_ACTIVATION_DAYS+1
        )
        self.assertEqual(profile.status, 'expired')
        self.assertEqual(profile.activation_key_expired(), True)

    def test_send_registration_email(self):
        new_user = self.create_inactive_user()
        profile = RegistrationProfile.objects.create(user=new_user)
        profile.send_registration_email(site=self.mock_site)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user_info['email']])

    def test_send_activation_email(self):
        new_user = self.create_inactive_user()
        profile = RegistrationProfile.objects.create(user=new_user)
        profile.send_activation_email(site=self.mock_site)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user_info['email']])

    def test_send_acceptance_email(self):
        new_user = self.create_inactive_user()
        profile = RegistrationProfile.objects.create(user=new_user)
        profile.send_acceptance_email(site=self.mock_site)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user_info['email']])

    def test_send_rejection_email(self):
        new_user = self.create_inactive_user()
        profile = RegistrationProfile.objects.create(user=new_user)
        profile.status = 'rejected'
        profile.save()
        profile.send_rejection_email(site=self.mock_site)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user_info['email']])


@override_settings(
    ACCOUNT_ACTIVATION_DAYS=7,
    REGISTRATION_OPEN=True,
    REGISTRATION_SUPPLEMENT_CLASS=None,
    REGISTRATION_BACKEND_CLASS=(
        'registration.backends.default.DefaultRegistrationBackend'),
)
class RegistrationProfileManagerTestCase(TestCase):
    user_info = {
        'username': 'alice',
        'email': 'alice@example.com',
    }

    def setUp(self):
        self.mock_site = mock_site()

    def test_register(self):
        new_user = RegistrationProfile.objects.register(site=self.mock_site,
                                                        **self.user_info)
        self.assertEqual(new_user.username, 'alice')
        self.assertEqual(new_user.email, 'alice@example.com')
        self.failIf(new_user.is_active)
        self.failIf(new_user.has_usable_password())

    def test_register_email(self):
        RegistrationProfile.objects.register(site=self.mock_site,
                                             **self.user_info)

        self.assertEqual(len(mail.outbox), 1)

    def test_register_no_email(self):
        RegistrationProfile.objects.register(site=self.mock_site,
                                             send_email=False,
                                             **self.user_info)

        self.assertEqual(len(mail.outbox), 0)

    def test_acceptance(self):
        new_user = RegistrationProfile.objects.register(site=self.mock_site,
                                                        send_email=False,
                                                        **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.accept_registration(profile,
                                                        site=self.mock_site)

        self.assertEqual(profile.status, 'accepted')
        self.assertNotEqual(profile.activation_key, None)

    def test_acceptance_email(self):
        new_user = RegistrationProfile.objects.register(site=self.mock_site,
                                                        send_email=False,
                                                        **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.accept_registration(profile,
                                                        site=self.mock_site)

        self.assertEqual(len(mail.outbox), 1)

    def test_acceptance_no_email(self):
        new_user = RegistrationProfile.objects.register(site=self.mock_site,
                                                        send_email=False,
                                                        **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.accept_registration(profile,
                                                        site=self.mock_site,
                                                        send_email=False)

        self.assertEqual(len(mail.outbox), 0)

    def test_acceptance_force(self):
        user1 = RegistrationProfile.objects.register(
            username='user1', email='user1@example.com',
            site=self.mock_site, send_email=False,
        )
        user2 = RegistrationProfile.objects.register(
            username='user2', email='user2@example.com',
            site=self.mock_site, send_email=False,
        )
        RegistrationProfile.objects.accept_registration(
            user1.registration_profile, site=self.mock_site
        )
        RegistrationProfile.objects.reject_registration(
            user2.registration_profile, site=self.mock_site
        )

        # from accepted => accepted
        profile = user1.registration_profile
        previous_activation_key = profile.activation_key
        RegistrationProfile.objects.accept_registration(profile,
                                                        site=self.mock_site,
                                                        force=True)
        self.assertEqual(profile.status, 'accepted')
        self.assertNotEqual(profile.activation_key, previous_activation_key)

        # from rejected => accepted
        profile = user2.registration_profile
        RegistrationProfile.objects.accept_registration(profile,
                                                        site=self.mock_site,
                                                        force=True)
        self.assertEqual(profile.status, 'accepted')
        self.assertNotEqual(profile.activation_key, None)

    def test_rejection(self):
        new_user = RegistrationProfile.objects.register(site=self.mock_site,
                                                        send_email=False,
                                                        **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.reject_registration(profile,
                                                        site=self.mock_site)

        self.assertEqual(profile.status, 'rejected')
        self.assertEqual(profile.activation_key, None)

    def test_rejection_email(self):
        new_user = RegistrationProfile.objects.register(site=self.mock_site,
                                                        send_email=False,
                                                        **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.reject_registration(profile,
                                                        site=self.mock_site)

        self.assertEqual(len(mail.outbox), 1)

    def test_rejection_no_email(self):
        new_user = RegistrationProfile.objects.register(site=self.mock_site,
                                                        send_email=False,
                                                        **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.reject_registration(profile,
                                                        site=self.mock_site,
                                                        send_email=False)

        self.assertEqual(len(mail.outbox), 0)

    def test_acceptance_after_rejection_success(self):
        new_user = RegistrationProfile.objects.register(site=self.mock_site,
                                                        send_email=False,
                                                        **self.user_info)

        profile = new_user.registration_profile

        # reject
        result = RegistrationProfile.objects.reject_registration(
            profile, site=self.mock_site
        )
        self.failUnless(result)
        self.assertEqual(profile.status, 'rejected')
        self.assertEqual(profile.activation_key, None)

        # accept should work even after rejection
        result = RegistrationProfile.objects.accept_registration(
            profile, site=self.mock_site
        )
        self.failUnless(result)
        self.assertEqual(profile.status, 'accepted')
        self.assertNotEqual(profile.activation_key, None)

    def test_acceptance_after_acceptance_fail(self):
        new_user = RegistrationProfile.objects.register(site=self.mock_site,
                                                        send_email=False,
                                                        **self.user_info)

        profile = new_user.registration_profile

        # accept
        result = RegistrationProfile.objects.accept_registration(
            profile, site=self.mock_site
        )
        self.failUnless(result)
        self.assertEqual(profile.status, 'accepted')
        self.assertNotEqual(profile.activation_key, None)

        # accept should not work
        result = RegistrationProfile.objects.accept_registration(
            profile, site=self.mock_site
        )
        self.failIf(result)
        self.assertEqual(profile.status, 'accepted')
        self.assertNotEqual(profile.activation_key, None)

    def test_rejection_after_acceptance_fail(self):
        new_user = RegistrationProfile.objects.register(site=self.mock_site,
                                                        send_email=False,
                                                        **self.user_info)

        profile = new_user.registration_profile

        # accept
        result = RegistrationProfile.objects.accept_registration(
            profile, site=self.mock_site
        )
        self.failUnless(result)
        self.assertEqual(profile.status, 'accepted')
        self.assertNotEqual(profile.activation_key, None)

        # reject should not work
        result = RegistrationProfile.objects.reject_registration(
            profile, site=self.mock_site
        )
        self.failIf(result)
        self.assertEqual(profile.status, 'accepted')
        self.assertNotEqual(profile.activation_key, None)

    def test_rejection_after_rejection_fail(self):
        new_user = RegistrationProfile.objects.register(site=self.mock_site,
                                                        send_email=False,
                                                        **self.user_info)

        profile = new_user.registration_profile

        # accept
        result = RegistrationProfile.objects.reject_registration(
            profile, site=self.mock_site
        )
        self.failUnless(result)
        self.assertEqual(profile.status, 'rejected')
        self.assertEqual(profile.activation_key, None)

        # reject should not work
        result = RegistrationProfile.objects.reject_registration(
            profile, site=self.mock_site
        )
        self.failIf(result)
        self.assertEqual(profile.status, 'rejected')
        self.assertEqual(profile.activation_key, None)

    def test_activation_with_password(self):
        new_user = RegistrationProfile.objects.register(site=self.mock_site,
                                                        send_email=False,
                                                        **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.accept_registration(
            profile, site=self.mock_site, send_email=False
        )
        activated = RegistrationProfile.objects.activate_user(
                activation_key=profile.activation_key,
                site=self.mock_site,
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
        new_user = RegistrationProfile.objects.register(site=self.mock_site,
                                                        send_email=False,
                                                        **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.accept_registration(
            profile, site=self.mock_site, send_email=False
        )
        activated = RegistrationProfile.objects.activate_user(
            activation_key=profile.activation_key,
            site=self.mock_site,
            send_email=False
        )

        self.failUnless(activated)

        activated_user, password, is_generated = activated

        self.assertEqual(new_user, activated_user)
        self.assertEqual(len(password),
                         settings.REGISTRATION_DEFAULT_PASSWORD_LENGTH)
        self.assertEqual(is_generated, True)
        # the user should be activated with the password
        self.failUnless(activated_user.is_active)
        self.failUnless(activated_user.has_usable_password())
        self.failUnless(activated_user.check_password(password))
        # inspection profile should be deleted
        self.failIf(RegistrationProfile.objects.filter(pk=profile.pk).exists())

    def test_activation_email(self):
        new_user = RegistrationProfile.objects.register(site=self.mock_site,
                                                        send_email=False,
                                                        **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.accept_registration(
            profile, site=self.mock_site, send_email=False
        )
        RegistrationProfile.objects.activate_user(
            activation_key=profile.activation_key,
            site=self.mock_site,
        )

        self.assertEqual(len(mail.outbox), 1)

    def test_activation_no_email(self):
        new_user = RegistrationProfile.objects.register(site=self.mock_site,
                                                        send_email=False,
                                                        **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.accept_registration(
            profile, site=self.mock_site, send_email=False
        )
        RegistrationProfile.objects.activate_user(
            activation_key=profile.activation_key,
            site=self.mock_site,
            send_email=False
        )

        self.assertEqual(len(mail.outbox), 0)

    def test_activation_with_untreated_fail(self):
        new_user = RegistrationProfile.objects.register(site=self.mock_site,
                                                        send_email=False,
                                                        **self.user_info)

        profile = new_user.registration_profile

        result = RegistrationProfile.objects.activate_user(
            activation_key=profile.activation_key,
            site=self.mock_site,
            password='swordfish'
        )

        self.failIf(result)
        # the user should not be activated
        self.failIf(new_user.is_active)
        self.failIf(new_user.has_usable_password())
        self.failIf(new_user.check_password('swordfish'))
        # inspection profile should not be deleted
        self.failUnless(
            RegistrationProfile.objects.filter(pk=profile.pk).exists()
        )

    def test_activation_with_rejected_fail(self):
        new_user = RegistrationProfile.objects.register(site=self.mock_site,
                                                        send_email=False,
                                                        **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.reject_registration(
            profile, site=self.mock_site
        )

        result = RegistrationProfile.objects.activate_user(
            activation_key=profile.activation_key,
            site=self.mock_site,
            password='swordfish'
        )

        self.failIf(result)
        # the user should not be activated
        self.failIf(new_user.is_active)
        self.failIf(new_user.has_usable_password())
        self.failIf(new_user.check_password('swordfish'))
        # inspection profile should not be deleted
        self.failUnless(
            RegistrationProfile.objects.filter(pk=profile.pk).exists()
        )

    def test_activation_with_expired_fail(self):
        new_user = RegistrationProfile.objects.register(site=self.mock_site,
                                                        send_email=False,
                                                        **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.accept_registration(
            profile, site=self.mock_site
        )

        new_user.date_joined -= datetime.timedelta(
            days=settings.ACCOUNT_ACTIVATION_DAYS + 1
        )
        new_user.save()

        result = RegistrationProfile.objects.activate_user(
            activation_key=profile.activation_key,
            site=self.mock_site,
            password='swordfish'
        )

        self.failIf(result)
        # the user should not be activated
        self.failIf(new_user.is_active)
        self.failIf(new_user.has_usable_password())
        self.failIf(new_user.check_password('swordfish'))
        # inspection profile should not be deleted
        self.failUnless(
            RegistrationProfile.objects.filter(pk=profile.pk).exists()
        )

    def test_activation_with_invalid_key_fail(self):
        new_user = RegistrationProfile.objects.register(site=self.mock_site,
                                                        send_email=False,
                                                        **self.user_info)

        profile = new_user.registration_profile
        RegistrationProfile.objects.accept_registration(
            profile, site=self.mock_site
        )

        result = RegistrationProfile.objects.activate_user(
            activation_key='foo',
            site=self.mock_site,
            password='swordfish'
        )

        self.failIf(result)
        # the user should not be activated
        self.failIf(new_user.is_active)
        self.failIf(new_user.has_usable_password())
        self.failIf(new_user.check_password('swordfish'))
        # inspection profile should not be deleted
        self.failUnless(
            RegistrationProfile.objects.filter(pk=profile.pk).exists()
        )

    def test_expired_user_deletion(self):
        RegistrationProfile.objects.register(
            username='new_untreated_user',
            email='new_untreated_user@example.com',
            site=self.mock_site,
        )
        new_accepted_user = RegistrationProfile.objects.register(
            username='new_accepted_user',
            email='new_accepted_user@example.com',
            site=self.mock_site,
        )
        new_rejected_user = RegistrationProfile.objects.register(
            username='new_rejected_user',
            email='new_rejected_user@example.com',
            site=self.mock_site,
        )
        expired_untreated_user = RegistrationProfile.objects.register(
            username='expired untreated user',
            email='expired_untreated_user@example.com',
            site=self.mock_site,
        )
        expired_accepted_user = RegistrationProfile.objects.register(
            username='expired_accepted_user',
            email='expired_accepted_user@example.com',
            site=self.mock_site,
        )
        expired_rejected_user = RegistrationProfile.objects.register(
            username='expired_rejected_user',
            email='expired_rejected_user@example.com',
            site=self.mock_site,
        )

        RegistrationProfile.objects.accept_registration(
            new_accepted_user.registration_profile,
            site=self.mock_site,
        )
        RegistrationProfile.objects.reject_registration(
            new_rejected_user.registration_profile,
            site=self.mock_site,
        )
        RegistrationProfile.objects.accept_registration(
            expired_accepted_user.registration_profile,
            site=self.mock_site,
        )
        RegistrationProfile.objects.reject_registration(
            expired_rejected_user.registration_profile,
            site=self.mock_site,
        )

        delta = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS+1)

        expired_untreated_user.date_joined -= delta
        expired_untreated_user.save()
        expired_accepted_user.date_joined -= delta
        expired_accepted_user.save()
        expired_rejected_user.date_joined -= delta
        expired_rejected_user.save()

        RegistrationProfile.objects.delete_expired_users()
        # Only expired_accepted_user is deleted
        User = get_user_model()
        self.assertEqual(RegistrationProfile.objects.count(), 5)
        self.assertRaises(User.DoesNotExist,
                          User.objects.get,
                          username='expired_accepted_user')

    def test_rejected_user_deletion(self):
        RegistrationProfile.objects.register(
            username='new_untreated_user',
            email='new_untreated_user@example.com',
            site=self.mock_site,
        )
        new_accepted_user = RegistrationProfile.objects.register(
            username='new_accepted_user',
            email='new_accepted_user@example.com',
            site=self.mock_site,
        )
        new_rejected_user = RegistrationProfile.objects.register(
            username='new_rejected_user',
            email='new_rejected_user@example.com',
            site=self.mock_site,
        )
        expired_untreated_user = RegistrationProfile.objects.register(
            username='expired untreated user',
            email='expired_untreated_user@example.com',
            site=self.mock_site,
        )
        expired_accepted_user = RegistrationProfile.objects.register(
            username='expired_accepted_user',
            email='expired_accepted_user@example.com',
            site=self.mock_site,
        )
        expired_rejected_user = RegistrationProfile.objects.register(
            username='expired_rejected_user',
            email='expired_rejected_user@example.com',
            site=self.mock_site,
        )

        RegistrationProfile.objects.accept_registration(
            new_accepted_user.registration_profile,
            site=self.mock_site,
        )
        RegistrationProfile.objects.reject_registration(
            new_rejected_user.registration_profile,
            site=self.mock_site,
        )
        RegistrationProfile.objects.accept_registration(
            expired_accepted_user.registration_profile,
            site=self.mock_site,
        )
        RegistrationProfile.objects.reject_registration(
            expired_rejected_user.registration_profile,
            site=self.mock_site,
        )

        delta = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS+1)

        expired_untreated_user.date_joined -= delta
        expired_untreated_user.save()
        expired_accepted_user.date_joined -= delta
        expired_accepted_user.save()
        expired_rejected_user.date_joined -= delta
        expired_rejected_user.save()

        RegistrationProfile.objects.delete_rejected_users()
        # new_rejected_user and expired_rejected_user are deleted
        User = get_user_model()
        self.assertEqual(RegistrationProfile.objects.count(), 4)
        self.assertRaises(User.DoesNotExist,
                          User.objects.get,
                          username='new_rejected_user')
        self.assertRaises(User.DoesNotExist,
                          User.objects.get,
                          username='expired_rejected_user')

    def test_management_command_cleanup_expired_registrations(self):
        RegistrationProfile.objects.register(
            username='new_untreated_user',
            email='new_untreated_user@example.com',
            site=self.mock_site,
        )
        new_accepted_user = RegistrationProfile.objects.register(
            username='new_accepted_user',
            email='new_accepted_user@example.com',
            site=self.mock_site,
        )
        new_rejected_user = RegistrationProfile.objects.register(
            username='new_rejected_user',
            email='new_rejected_user@example.com',
            site=self.mock_site,
        )
        expired_untreated_user = RegistrationProfile.objects.register(
            username='expired untreated user',
            email='expired_untreated_user@example.com',
            site=self.mock_site,
        )
        expired_accepted_user = RegistrationProfile.objects.register(
            username='expired_accepted_user',
            email='expired_accepted_user@example.com',
            site=self.mock_site,
        )
        expired_rejected_user = RegistrationProfile.objects.register(
            username='expired_rejected_user',
            email='expired_rejected_user@example.com',
            site=self.mock_site,
        )

        RegistrationProfile.objects.accept_registration(
            new_accepted_user.registration_profile,
            site=self.mock_site,
        )
        RegistrationProfile.objects.reject_registration(
            new_rejected_user.registration_profile,
            site=self.mock_site,
        )
        RegistrationProfile.objects.accept_registration(
            expired_accepted_user.registration_profile,
            site=self.mock_site,
        )
        RegistrationProfile.objects.reject_registration(
            expired_rejected_user.registration_profile,
            site=self.mock_site,
        )

        delta = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS+1)

        expired_untreated_user.date_joined -= delta
        expired_untreated_user.save()
        expired_accepted_user.date_joined -= delta
        expired_accepted_user.save()
        expired_rejected_user.date_joined -= delta
        expired_rejected_user.save()

        management.call_command('cleanup_expired_registrations')
        # Only expired_accepted_user is deleted
        User = get_user_model()
        self.assertEqual(RegistrationProfile.objects.count(), 5)
        self.assertRaises(User.DoesNotExist, User.objects.get,
                          username='expired_accepted_user')

    def test_management_command_cleanup_rejected_registrations(self):
        RegistrationProfile.objects.register(
            username='new_untreated_user',
            email='new_untreated_user@example.com',
            site=self.mock_site,
        )
        new_accepted_user = RegistrationProfile.objects.register(
            username='new_accepted_user',
            email='new_accepted_user@example.com',
            site=self.mock_site,
        )
        new_rejected_user = RegistrationProfile.objects.register(
            username='new_rejected_user',
            email='new_rejected_user@example.com',
            site=self.mock_site,
        )
        expired_untreated_user = RegistrationProfile.objects.register(
            username='expired untreated user',
            email='expired_untreated_user@example.com',
            site=self.mock_site,
        )
        expired_accepted_user = RegistrationProfile.objects.register(
            username='expired_accepted_user',
            email='expired_accepted_user@example.com',
            site=self.mock_site,
        )
        expired_rejected_user = RegistrationProfile.objects.register(
            username='expired_rejected_user',
            email='expired_rejected_user@example.com',
            site=self.mock_site,
        )

        RegistrationProfile.objects.accept_registration(
            new_accepted_user.registration_profile,
            site=self.mock_site,
        )
        RegistrationProfile.objects.reject_registration(
            new_rejected_user.registration_profile,
            site=self.mock_site,
        )
        RegistrationProfile.objects.accept_registration(
            expired_accepted_user.registration_profile,
            site=self.mock_site,
        )
        RegistrationProfile.objects.reject_registration(
            expired_rejected_user.registration_profile,
            site=self.mock_site,
        )

        delta = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS+1)

        expired_untreated_user.date_joined -= delta
        expired_untreated_user.save()
        expired_accepted_user.date_joined -= delta
        expired_accepted_user.save()
        expired_rejected_user.date_joined -= delta
        expired_rejected_user.save()

        management.call_command('cleanup_rejected_registrations')
        # new_rejected_user and expired_rejected_user are deleted
        User = get_user_model()
        self.assertEqual(RegistrationProfile.objects.count(), 4)
        self.assertRaises(User.DoesNotExist, User.objects.get,
                          username='new_rejected_user')
        self.assertRaises(User.DoesNotExist, User.objects.get,
                          username='expired_rejected_user')

    def test_management_command_cleanup_registrations(self):
        RegistrationProfile.objects.register(
            username='new_untreated_user',
            email='new_untreated_user@example.com',
            site=self.mock_site,
        )
        new_accepted_user = RegistrationProfile.objects.register(
            username='new_accepted_user',
            email='new_accepted_user@example.com',
            site=self.mock_site,
        )
        new_rejected_user = RegistrationProfile.objects.register(
            username='new_rejected_user',
            email='new_rejected_user@example.com',
            site=self.mock_site,
        )
        expired_untreated_user = RegistrationProfile.objects.register(
            username='expired untreated user',
            email='expired_untreated_user@example.com',
            site=self.mock_site,
        )
        expired_accepted_user = RegistrationProfile.objects.register(
            username='expired_accepted_user',
            email='expired_accepted_user@example.com',
            site=self.mock_site,
        )
        expired_rejected_user = RegistrationProfile.objects.register(
            username='expired_rejected_user',
            email='expired_rejected_user@example.com',
            site=self.mock_site,
        )

        RegistrationProfile.objects.accept_registration(
            new_accepted_user.registration_profile,
            site=self.mock_site,
        )
        RegistrationProfile.objects.reject_registration(
            new_rejected_user.registration_profile,
            site=self.mock_site,
        )
        RegistrationProfile.objects.accept_registration(
            expired_accepted_user.registration_profile,
            site=self.mock_site,
        )
        RegistrationProfile.objects.reject_registration(
            expired_rejected_user.registration_profile,
            site=self.mock_site,
        )

        delta = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS+1)

        expired_untreated_user.date_joined -= delta
        expired_untreated_user.save()
        expired_accepted_user.date_joined -= delta
        expired_accepted_user.save()
        expired_rejected_user.date_joined -= delta
        expired_rejected_user.save()

        management.call_command('cleanup_registrations')
        # new_rejected_user, expired rejected_user and expired_accepted_user
        # are deleted
        User = get_user_model()
        self.assertEqual(RegistrationProfile.objects.count(), 3)
        self.assertRaises(User.DoesNotExist, User.objects.get,
                          username='new_rejected_user')
        self.assertRaises(User.DoesNotExist, User.objects.get,
                          username='expired_rejected_user')
        self.assertRaises(User.DoesNotExist, User.objects.get,
                          username='expired_accepted_user')

    def test_management_command_cleanupregistration(self):
        RegistrationProfile.objects.register(
            username='new_untreated_user',
            email='new_untreated_user@example.com',
            site=self.mock_site,
        )
        new_accepted_user = RegistrationProfile.objects.register(
            username='new_accepted_user',
            email='new_accepted_user@example.com',
            site=self.mock_site,
        )
        new_rejected_user = RegistrationProfile.objects.register(
            username='new_rejected_user',
            email='new_rejected_user@example.com',
            site=self.mock_site,
        )
        expired_untreated_user = RegistrationProfile.objects.register(
            username='expired untreated user',
            email='expired_untreated_user@example.com',
            site=self.mock_site,
        )
        expired_accepted_user = RegistrationProfile.objects.register(
            username='expired_accepted_user',
            email='expired_accepted_user@example.com',
            site=self.mock_site,
        )
        expired_rejected_user = RegistrationProfile.objects.register(
            username='expired_rejected_user',
            email='expired_rejected_user@example.com',
            site=self.mock_site,
        )

        RegistrationProfile.objects.accept_registration(
            new_accepted_user.registration_profile,
            site=self.mock_site,
        )
        RegistrationProfile.objects.reject_registration(
            new_rejected_user.registration_profile,
            site=self.mock_site,
        )
        RegistrationProfile.objects.accept_registration(
            expired_accepted_user.registration_profile,
            site=self.mock_site,
        )
        RegistrationProfile.objects.reject_registration(
            expired_rejected_user.registration_profile,
            site=self.mock_site,
        )

        delta = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS+1)

        expired_untreated_user.date_joined -= delta
        expired_untreated_user.save()
        expired_accepted_user.date_joined -= delta
        expired_accepted_user.save()
        expired_rejected_user.date_joined -= delta
        expired_rejected_user.save()

        # django-registration compatibility
        management.call_command('cleanupregistration')
        # new_rejected_user, expired rejected_user and expired_accepted_user
        # are deleted
        User = get_user_model()
        self.assertEqual(RegistrationProfile.objects.count(), 3)
        self.assertRaises(User.DoesNotExist, User.objects.get,
                          username='new_rejected_user')
        self.assertRaises(User.DoesNotExist, User.objects.get,
                          username='expired_rejected_user')
        self.assertRaises(User.DoesNotExist, User.objects.get,
                          username='expired_accepted_user')
