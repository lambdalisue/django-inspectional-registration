#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
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
from django.test import TestCase

from ..backends.default import DefaultRegistrationBackend
from mock import mock_request
from mock import mock_site

class RegistrationTestCaseBase(TestCase):
    # I'm not sure but I now think setting urls is not
    # good idea for re-usable app.
    #urls = 'registration.tests.urls'
    backend = DefaultRegistrationBackend()

    _test_settings = (
        ('ACCOUNT_ACTIVATION_DAYS', 7),
        ('REGISTRATION_OPEN', True),
        ('REGISTRATION_BACKEND_CLASS', 'registration.backends.default.DefaultRegistrationBackend'),
        ('REGISTRATION_SUPPLEMENT_CLASS', None),
    )

    def _store_and_overwrite_settings(self, name_and_values):
        """store named settings to this instance and overwrite the settings"""
        for value in name_and_values:
            name, value = value
            cache = getattr(settings, name)
            setattr(self, "_%s_cache" % name.lower(), cache)
            setattr(settings, name, value)

    def _restore_settings(self, name_and_values):
        """restore named settings from this instance"""
        for value in name_and_values:
            name, value = value
            cache = getattr(self, "_%s_cache" % name.lower())
            setattr(self, name, cache)

    def setUp(self):
        self._store_and_overwrite_settings(self._test_settings)
        self.mock_request = mock_request()
        self.mock_site = mock_site()

    def tearDown(self):
        self._restore_settings(self._test_settings)
