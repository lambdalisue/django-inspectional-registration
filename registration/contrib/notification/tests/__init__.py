#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
"""
Unittest of registration.contrib.notification


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
from django.core import mail

from registration.tests import RegistrationTestCaseBase

class RegistrationNotificationTestCase(RegistrationTestCaseBase):
    #urls = 'registration.contrib.notification.tests.urls'

    test_settings = (
        ('ADMINS', (
                ('admin1', 'admin1@test.com'),
                ('admin2', 'admin2@test.com'),
        )),
        ('MANAGERS', (
            ('manager1', 'manager1@test.com'), 
            ('manager2', 'manager2@test.com'),
        )),
        ('REGISTRATION_NOTIFICATION', True),
        ('REGISTRATION_NOTIFICATION_ADMINS', True),
        ('REGISTRATION_NOTIFICATION_MANAGERS', True),
        ('REGISTRATION_NOTIFICATION_RECIPIENTS', None),
        # disable the registration email
        ('REGISTRATION_REGISTRATION_EMAIL', False),
    )

    def setUp(self):
        super(RegistrationNotificationTestCase, self).setUp()
        self._store_and_overwrite_settings(self.test_settings)
        settings._REGISTRATION_NOTIFICATION_IN_TESTS = True

    def tearDown(self):
        super(RegistrationNotificationTestCase, self).tearDown()
        self._restore_settings(self.test_settings)
        del settings._REGISTRATION_NOTIFICATION_IN_TESTS

    def test_notify_admins(self):
        settings.REGISTRATION_NOTIFICATION_MANAGERS = False
        
        self.backend.register(
                'bob', 'bob@test.com', request=self.mock_request
            )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(sorted(mail.outbox[0].to), sorted([
                'admin1@test.com',
                'admin2@test.com',
            ]))

    def test_notify_managers(self):
        settings.REGISTRATION_NOTIFICATION_ADMINS = False
        
        self.backend.register(
                'bob', 'bob@test.com', request=self.mock_request
            )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(sorted(mail.outbox[0].to), sorted([
                'manager1@test.com',
                'manager2@test.com',
            ]))

    def test_notify_recipients_iterable(self):
        settings.REGISTRATION_NOTIFICATION_ADMINS = False
        settings.REGISTRATION_NOTIFICATION_MANAGERS = False
        settings.REGISTRATION_NOTIFICATION_RECIPIENTS = (
                'recipient1@test.com',
                'recipient2@test.com',
            )
        
        self.backend.register(
                'bob', 'bob@test.com', request=self.mock_request
            )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(sorted(mail.outbox[0].to), sorted([
                'recipient1@test.com',
                'recipient2@test.com',
            ]))

    def test_notify_recipients_function(self):
        settings.REGISTRATION_NOTIFICATION_ADMINS = False
        settings.REGISTRATION_NOTIFICATION_MANAGERS = False
        settings.REGISTRATION_NOTIFICATION_RECIPIENTS = lambda : (
                'recipient1@test.com',
                'recipient2@test.com',
            )
        
        self.backend.register(
                'bob', 'bob@test.com', request=self.mock_request
            )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(sorted(mail.outbox[0].to), sorted([
                'recipient1@test.com',
                'recipient2@test.com',
            ]))

    def test_notify_all(self):
        settings.REGISTRATION_NOTIFICATION_ADMINS = True
        settings.REGISTRATION_NOTIFICATION_MANAGERS = True
        settings.REGISTRATION_NOTIFICATION_RECIPIENTS = (
                'recipient1@test.com',
                'recipient2@test.com',
            )
        
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
        settings.REGISTRATION_NOTIFICATION_ADMINS = True
        settings.REGISTRATION_NOTIFICATION_MANAGERS = True
        settings.REGISTRATION_NOTIFICATION_RECIPIENTS = (
                'admin1@test.com',
                'admin2@test.com',
                'manager1@test.com',
                'manager2@test.com',
                'recipient1@test.com',
                'recipient2@test.com',
            )
        settings.ADMINS = (
            ('admin1', 'admin1@test.com'),
            ('admin2', 'admin2@test.com'),
            ('manager1', 'manager1@test.com'), 
            ('manager2', 'manager2@test.com'),
            ('recipient1', 'recipient1@test.com'), 
            ('recipient2', 'recipient2@test.com'),
        )
        settings.MANAGERS = (
            ('admin1', 'admin1@test.com'),
            ('admin2', 'admin2@test.com'),
            ('manager1', 'manager1@test.com'), 
            ('manager2', 'manager2@test.com'),
            ('recipient1', 'recipient1@test.com'), 
            ('recipient2', 'recipient2@test.com'),
        )

        
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
