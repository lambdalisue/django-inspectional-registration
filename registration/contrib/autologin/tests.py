#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
"""
Unittest of autologin


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
from __future__ import with_statement
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser

from registration.backends.default import DefaultRegistrationBackend
from registration.tests.override_settings import override_settings
from registration.tests.mock import mock_request

@override_settings(
        ACCOUNT_ACTIVATION_DAYS=7,
        REGISTRATION_OPEN=True,
        REGISTRATION_SUPPLEMENT_CLASS=None,
        REGISTRATION_BACKEND_CLASS='registration.backends.default.DefaultRegistrationBackend',
        REGISTRATION_AUTO_LOGIN=True,
        _REGISTRATION_AUTO_LOGIN_IN_TESTS=True,
    )
class RegistrationAutoLoginTestCase(TestCase):
    backend = DefaultRegistrationBackend()
    mock_request = mock_request()

    def test_no_auto_login_with_setting(self):
        """Auto login feature should be able to off with ``REGISTRATION_AUTO_LOGIN = False``"""
        self.mock_request.user = AnonymousUser()

        with override_settings(REGISTRATION_AUTO_LOGIN = False):

            new_user = self.backend.register(
                    'bob', 'bob@test.com', request=self.mock_request,
                )
            self.backend.accept(
                    new_user.registration_profile, request=self.mock_request,
                )
            self.backend.activate(
                    new_user.registration_profile.activation_key,
                    password='password',request=self.mock_request,
                )

            self.failIf(self.mock_request.user.is_authenticated())

    def test_no_auto_login_with_no_password(self):
        """Auto login feature should not be occur with no password 
        (programatically activated by Django Admin action)
        
        """
        self.mock_request.user = AnonymousUser()

        new_user = self.backend.register(
                'bob', 'bob@test.com', request=self.mock_request,
            )
        self.backend.accept(
                new_user.registration_profile, request=self.mock_request,
            )
        self.backend.activate(
                new_user.registration_profile.activation_key,
                request=self.mock_request,
            )

        self.failIf(self.mock_request.user.is_authenticated())

    def test_auto_login(self):
        """Wheather auto login feature works correctly"""
        self.mock_request.user = AnonymousUser()

        new_user = self.backend.register(
                'bob', 'bob@test.com', request=self.mock_request,
            )
        self.backend.accept(
                new_user.registration_profile, request=self.mock_request,
            )
        self.backend.activate(
                new_user.registration_profile.activation_key,
                password='password',request=self.mock_request,
            )

        self.failUnless(self.mock_request.user.is_authenticated())
