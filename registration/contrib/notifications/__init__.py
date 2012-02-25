#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Send a notification emails to admins/managers when new user has registered

admin/manager will be determined from ``ADMINS`` and ``MANAGERS`` attribute of
``settings.py``

You can disable this feature by setting ``False`` to ``REGISTRATION_NOTIFICATION_EMAIL``
and you can disable sending email to admin by ``REGISTRATION_NOTIFICATION_EMAIL_ADMIN``
and you can disable sending email to manager by ``REGISTRATION_NOTIFICATION_EMAIL_MANAGER``

If you need extra email address to recive the notification emails, add the email address
to ``REGISTRATION_NOTIFICATION_EXTRA_RECIPIENTS``


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
from django.template.loader import render_to_string

from utils import get_site
from utils import send_mail
from signals import user_registered

def setconf(name, default_value):
    """set default value to django.conf.settings"""
    value = getattr(settings, name, default_value)
    setattr(settings, name, value)

setconf('REGISTRATION_NOTIFICATION_EMAIL', True)
setconf('REGISTRATION_NOTIFICATION_EMAIL_ADMIN', True)
setconf('REGISTRATION_NOTIFICATION_EMAIL_MANAGER', True)
setconf('REGISTRATION_NOTIFICATION_EXTRA_RECIPIENTS', [])

def send_notification_email(sender, user, profile, request, **kwargs):
    """send a notification email to admins/managers"""
    template_name = r"registration/notification_email.txt"
    template_subject_name = r"registration/notification_email_subject.txt"

    context = {
            'user': user,
            'profile': profile,
            'site': get_site(request),
        }
    subject = render_to_string(template_subject_name, context)
    subject = "".join(subject.splitlines())
    message = render_to_string(template_name, context)

    recipients = []
    if settings.REGISTRATION_NOTIFICATION_EMAIL_ADMIN:
        for userinfo in settings.ADMINS:
            recipients.append(userinfo[1])
    if settings.REGISTRATION_NOTIFICATION_EMAIL_MANAGER:
        for userinfo in settings.MANAGERS:
            recipients.append(userinfo[1])
    if settings.REGISTRATION_NOTIFICATION_EXTRA_RECIPIENTS:
        for recipient in settings.MANAGERS:
            recipients.append(recipient)
    # do not send same mail to same email address
    recipients = set(recipients)

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients)

if settings.REGISTRATION_NOTIFICATION:
    user_registered.connect(send_notification_email)
