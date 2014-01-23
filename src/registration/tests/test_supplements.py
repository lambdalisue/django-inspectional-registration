# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from django.core import mail
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured

from registration import forms
from registration.conf import settings
from registration.supplements import get_supplement_class
from registration.models import RegistrationProfile
from registration.tests.compat import override_settings


def with_apps(*apps):
    """
    Class decorator that makes sure the passed apps are present in
    INSTALLED_APPS.
    """
    apps_set = set(settings.INSTALLED_APPS)
    apps_set.update(apps)
    return override_settings(INSTALLED_APPS=list(apps_set))


class RegistrationSupplementRetrievalTests(TestCase):

    def test_get_supplement_class(self):
        from registration.supplements.default.models import DefaultRegistrationSupplement
        supplement_class = get_supplement_class(
                'registration.supplements.default.models.DefaultRegistrationSupplement')
        self.failUnless(supplement_class is DefaultRegistrationSupplement)

    def test_supplement_error_invalid(self):
        self.assertRaises(ImproperlyConfigured, get_supplement_class,
                'registration.supplements.doesnotexist.NonExistenBackend')

    def test_supplement_attribute_error(self):
        self.assertRaises(ImproperlyConfigured, get_supplement_class,
                'registration.supplements.default.NonexistenBackend')


@with_apps(
    'django.contrib.contenttypes',
    'registration.supplements.default'
)
@override_settings(
        ACCOUNT_ACTIVATION_DAYS=7,
        REGISTRATION_OPEN=True,
        REGISTRATION_SUPPLEMENT_CLASS=(
            'registration.supplements.default.models.DefaultRegistrationSupplement'),
        REGISTRATION_BACKEND_CLASS=(
            'registration.backends.default.DefaultRegistrationBackend'),
    )
class RegistrationViewWithDefaultRegistrationSupplementTestCase(TestCase):
    def setUp(self):
        from registration.tests.utils import recall_syncdb
        from registration.tests.utils import clear_all_meta_caches
        # recall syncdb
        recall_syncdb()
        # clear caches
        clear_all_meta_caches()
        from django.db.models import loading
        loading.cache.loaded = False

    def test_registration_view_get(self):
        """
        A ``GET`` to the ``register`` view uses the appropriate
        template and populates the registration form into the context.

        """
        from registration.supplements.default.models import DefaultRegistrationSupplement
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
        from registration.supplements.default.models import DefaultRegistrationSupplement
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
