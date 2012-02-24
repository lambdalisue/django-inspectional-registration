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
from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured

from .. import forms
from ..supplements import get_supplement_class
from ..supplements.default import DefaultRegistrationSupplement
from ..models import RegistrationProfile

from base import RegistrationTestCaseBase

class RegistrationSupplementRetrievalTests(RegistrationTestCaseBase):

    def test_get_supplement_class(self):
        supplement_class = get_supplement_class('registration.supplements.default.DefaultRegistrationSupplement')
        self.failUnless(supplement_class is DefaultRegistrationSupplement)

    def test_supplement_error_invalid(self):
        self.assertRaises(ImproperlyConfigured, get_supplement_class,
                'registration.supplements.doesnotexist.NonExistenBackend')

    def test_supplement_attribute_error(self):
        self.assertRaises(ImproperlyConfigured, get_supplement_class,
                'registration.supplements.default.NonexistenBackend')

class RegistrationViewWithDefaultRegistrationSupplementTestCase(RegistrationTestCaseBase):

    def setUp(self):
        super(RegistrationViewWithDefaultRegistrationSupplementTestCase, self).setUp()
        settings.REGISTRATION_SUPPLEMENT_CLASS = 'registration.supplements.default.DefaultRegistrationSupplement'

    def test_registration_view_get(self):
        """
        A ``GET`` to the ``register`` view uses the appropriate
        template and populates the registration form into the context.

        """
        response = self.client.get(reverse('registration_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'registration/registration_form.html')
        self.failUnless(isinstance(response.context['form'],
                                   forms.RegistrationForm))
        self.failUnless(isinstance(response.context['supplement_form'].instance,
                                   DefaultRegistrationSupplement))

    def test_registration_view_post_success(self):
        """
        A ``POST`` to the ``register`` view with valid data properly
        creates a new user and issues a redirect.

        """
        response = self.client.post(reverse('registration_register'),
                                    data={'username': 'alice',
                                          'email1': 'alice@example.com',
                                          'email2': 'alice@example.com',
                                          'remarks': 'Hello'})
        self.assertRedirects(response,
                             'http://testserver%s' % reverse('registration_complete'))
        self.assertEqual(RegistrationProfile.objects.count(), 1)
        self.assertEqual(DefaultRegistrationSupplement.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

        profile = RegistrationProfile.objects.get(user__username='alice')
        self.assertEqual(profile.supplement.remarks, 'Hello')

    def test_registration_view_post_failure(self):
        """
        A ``POST`` to the ``register`` view with invalid data does not
        create a user, and displays appropriate error messages.

        """
        response = self.client.post(reverse('registration_register'),
                                    data={'username': 'bob',
                                          'email1': 'bobe@example.com',
                                          'email2': 'mark@example.com',
                                          'remarks': 'Hello'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.failUnless(response.context['supplement_form'].is_valid())
        self.assertFormError(response, 'form', field=None,
                             errors=u"The two email fields didn't match.")
        self.assertEqual(len(mail.outbox), 0)

    def test_registration_view_post_no_remarks_failure(self):
        """
        A ``POST`` to the ``register`` view with invalid data does not
        create a user, and displays appropriate error messages.

        """
        response = self.client.post(reverse('registration_register'),
                                    data={'username': 'bob',
                                          'email1': 'bobe@example.com',
                                          'email2': 'bobe@example.com'})
        self.assertEqual(response.status_code, 200)
        self.failUnless(response.context['form'].is_valid())
        self.failIf(response.context['supplement_form'].is_valid())
        self.assertFormError(response, 'supplement_form', field='remarks',
                             errors=u"This field is required.")
        self.assertEqual(len(mail.outbox), 0)
