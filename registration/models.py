# vim: set fileencoding=utf8:
"""



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
__VERSION__ = "0.1.0"
import re
import datetime

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.utils.text import ugettext_lazy as _

from utils import generate_activation_key
from utils import generate_random_password

try:
    # Support Django 1.4 Timezone
    from django.utils.timezone import now as datetime_now
except ImportError:
    datetime_now = datetime.datetime.now

SHA1_RE = re.compile(r'^[a-f0-9]{40}$')

class RegistrationManager(models.Manager):

    def register(self, username, email, send_email=True):
        new_user = User.objects.create_user(username, email, 'password')
        new_user.set_unusable_password()
        new_user.is_active = False
        new_user.save()

        profile = self.create(user=new_user)

        if send_email:
            profile.send_registration_email()

        return new_user

    def accept_registration(self, profile, send_email=True):
        # rejected -> accepted is allowed
        if profile.status in ('untreated', 'rejected'):
            profile.status = 'accepted'
            profile.save()
            # update user's date_joined
            user = profile.user
            user.date_joined = datetime_now()
            user.save()

            if send_email:
                profile.send_acception_email()

            return profile.user
        return None

    def reject_registration(self, profile, send_email=True):
        # accepted -> rejected is not allowed
        if profile.status == 'untreated':
            profile.status = 'rejected'
            profile.save()

            if send_email:
                profile.send_rejection_email()

            return profile.user
        return None

    def activate_user(self, activation_key, password=None, send_email=True):
        try:
            profile = self.get(_status='accepted', activation_key=activation_key)
        except self.model.DoesNotExist:
            return None
        if not profile.activation_key_expired():
            is_generated = password is None
            password = password or generate_random_password(length=settings.REGISTRATION_DEFAULT_PASSWORD_LENGTH)
            user = profile.user
            user.set_password(password)
            user.is_active = True
            user.save()

            if send_email:
                profile.send_activation_email(password, is_generated)

            # the profile is no longer required
            profile.delete()
            return user, password, is_generated
        return None


    def delete_expired_users(self):
        for profile in self.all():
            if profile.activation_key_expired():
                user = profile.user
                user.delete()

    def delete_rejected_users(self):
        for profile in self.all():
            if profile.status == 'rejected':
                user = profile.user
                user.delete()


class RegistrationProfile(models.Model):
    STATUS_LIST = (
        ('untreated', _('Untreated yet')),
        ('accepted', _('Accepted')),
        ('rejected', _('Rejected')),
    )
    user = models.OneToOneField(User, verbose_name=_('user'), 
                                related_name='registration_profile', editable=False)
    _status = models.CharField(_('status'), max_length=10, db_column='status',
                              choices=STATUS_LIST, default='untreated', editable=False)
    activation_key = models.CharField(_('activation key'), max_length=40, null=True,
                                      default=None, editable=False)

    objects = RegistrationManager()

    class Meta:
        verbose_name = _('registration profile')
        verbose_name_plural = _('registration profiles')
        permissions = (
                ('accept_registrationprofile', 'Can accept user registration'),
                ('reject_registrationprofile', 'Can reject user registration'),
            )

    def _get_status(self):
        if self._status == 'accepted' and self.activation_key_expired():
            return 'expired'
        return self._status
    def _set_status(self, value):
        self._status = value
        # Automatically generate activation key for accepted profile
        if value == 'accepted' and not self.activation_key:
            username = self.user.username
            self.activation_key = generate_activation_key(username)
        elif value != 'accepted' and self.activation_key:
            self.activation_key = None
    status = property(_get_status, _set_status)

    def get_status_display(self):
        sl = list(self.STATUS_LIST)
        sl.append(('expired', _('Activation key has expired')))
        sl = dict(sl)
        return sl.get(self.status)

    def __unicode__(self):
        return u"Registration information for %s" % self.user

    def activation_key_expired(self):
        if self._status != 'accepted':
            return False
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        expired = self.user.date_joined + expiration_date <= datetime_now()
        return expired
    activation_key_expired.boolean = True

    def _create_email(self, action, extra_context=None):
        context = {
                'user': self.user,
                'profile': self,
                'site': Site.objects.get_current()
            }
        if extra_context:
            context.update(extra_context)

        subject = render_to_string('registration/%s_email_subject.txt' % action, context)
        subject = ''.join(subject.splitlines())
        message = render_to_string('registration/%s_email.txt' % action, context)

        return {'subject': subject, 'message': message, 'from_email': settings.DEFAULT_FROM_EMAIL}

    def send_registration_email(self):
        email = self._create_email('registration')
        self.user.email_user(**email)

    def send_acception_email(self):
        extra_context = {
                'activation_key': self.activation_key,
                'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
            }
        email = self._create_email('acception', extra_context)
        self.user.email_user(**email)

    def send_rejection_email(self):
        email = self._create_email('rejection')
        self.user.email_user(**email)

    def send_activation_email(self, password=None, generated=False):
        extra_context = {
                'password': password,
                'generated': generated,
            }
        email = self._create_email('activation', extra_context)
        self.user.email_user(**email)
