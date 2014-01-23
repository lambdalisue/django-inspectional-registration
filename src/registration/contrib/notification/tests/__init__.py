# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from django.conf import settings
from django.core import mail
from registration.backends.default import DefaultRegistrationBackend
from registration.tests.mock import mock_request
from registration.tests.compat import override_settings


@override_settings(
        ACCOUNT_ACTIVATION_DAYS=7,
        ADMINS=(
            ('admin1', 'admin1@test.com'),
            ('admin2', 'admin2@test.com'),
        ),
        MANAGERS=(
            ('manager1', 'manager1@test.com'), 
            ('manager2', 'manager2@test.com'),
        ),
        REGISTRATION_OPEN=True,
        REGISTRATION_SUPPLEMENT_CLASS=None,
        REGISTRATION_BACKEND_CLASS=(
            'registration.backends.default.DefaultRegistrationBackend'),
        REGISTRATION_REGISTRATION_EMAIL=False,
        REGISTRATION_NOTIFICATION=True,
        REGISTRATION_NOTIFICATION_ADMINS=True,
        REGISTRATION_NOTIFICATION_MANAGERS=True,
        REGISTRATION_NOTIFICATION_RECIPIENTS=False,
        _REGISTRATION_NOTIFICATION_IN_TESTS=True,
    )
class RegistrationNotificationTestCase(TestCase):
    backend = DefaultRegistrationBackend()
    mock_request = mock_request()

    def test_notify_admins(self):
        with override_settings(REGISTRATION_NOTIFICATION_MANAGERS=False):
            self.backend.register(
                    'bob', 'bob@test.com', request=self.mock_request
                )

            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(sorted(mail.outbox[0].to), sorted([
                    'admin1@test.com',
                    'admin2@test.com',
                ]))

    def test_notify_managers(self):
        with override_settings(REGISTRATION_NOTIFICATION_ADMINS=False):
            self.backend.register(
                    'bob', 'bob@test.com', request=self.mock_request
                )

            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(sorted(mail.outbox[0].to), sorted([
                    'manager1@test.com',
                    'manager2@test.com',
                ]))

    def test_notify_recipients_iterable(self):
        with override_settings(
            REGISTRATION_NOTIFICATION_ADMINS = False,
            REGISTRATION_NOTIFICATION_MANAGERS = False,
            REGISTRATION_NOTIFICATION_RECIPIENTS=(
                    'recipient1@test.com',
                    'recipient2@test.com',
                )):
            self.backend.register(
                    'bob', 'bob@test.com', request=self.mock_request
                )

            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(sorted(mail.outbox[0].to), sorted([
                    'recipient1@test.com',
                    'recipient2@test.com',
                ]))

    def test_notify_recipients_function(self):
        with override_settings(
            REGISTRATION_NOTIFICATION_ADMINS=False,
            REGISTRATION_NOTIFICATION_MANAGERS=False,
            REGISTRATION_NOTIFICATION_RECIPIENTS=lambda:(
                    'recipient1@test.com',
                    'recipient2@test.com',
                )):
            self.backend.register(
                    'bob', 'bob@test.com', request=self.mock_request
                )

            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(sorted(mail.outbox[0].to), sorted([
                    'recipient1@test.com',
                    'recipient2@test.com',
                ]))

    def test_notify_all(self):
        with override_settings(
            REGISTRATION_NOTIFICATION_ADMINS=True,
            REGISTRATION_NOTIFICATION_MANAGERS=True,
            REGISTRATION_NOTIFICATION_RECIPIENTS=(
                    'recipient1@test.com',
                    'recipient2@test.com',
                )):
            self.backend.register(
                    'bob', 'bob@test.com', request=self.mock_request
                )

            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(sorted(mail.outbox[0].to), sorted([
                    'admin1@test.com',
                    'admin2@test.com',
                    'manager1@test.com',
                    'manager2@test.com',
                    'recipient1@test.com',
                    'recipient2@test.com',
                ]))

    def test_notify_duplicated(self):
        with override_settings(
            REGISTRATION_NOTIFICATION_ADMINS=True,
            REGISTRATION_NOTIFICATION_MANAGERS=True,
            REGISTRATION_NOTIFICATION_RECIPIENTS=(
                    'admin1@test.com',
                    'admin2@test.com',
                    'manager1@test.com',
                    'manager2@test.com',
                    'recipient1@test.com',
                    'recipient2@test.com',
                ),
            ADMINS=(
                    ('admin1', 'admin1@test.com'),
                    ('admin2', 'admin2@test.com'),
                    ('manager1', 'manager1@test.com'), 
                    ('manager2', 'manager2@test.com'),
                    ('recipient1', 'recipient1@test.com'), 
                    ('recipient2', 'recipient2@test.com'),
                ),
            MANAGERS=(
                    ('admin1', 'admin1@test.com'),
                    ('admin2', 'admin2@test.com'),
                    ('manager1', 'manager1@test.com'), 
                    ('manager2', 'manager2@test.com'),
                    ('recipient1', 'recipient1@test.com'), 
                    ('recipient2', 'recipient2@test.com'),
                )):
            self.backend.register(
                    'bob', 'bob@test.com', request=self.mock_request
                )

            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(sorted(mail.outbox[0].to), sorted([
                    'admin1@test.com',
                    'admin2@test.com',
                    'manager1@test.com',
                    'manager2@test.com',
                    'recipient1@test.com',
                    'recipient2@test.com',
                ]))
