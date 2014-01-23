# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.conf import settings
from appconf import AppConf


class InspectionalRegistrationNotificationAppConf(AppConf):
    NOTIFICATION = True
    NOTIFICATION_ADMINS = True
    NOTIFICATION_MANAGERS = True
    NOTIFICATION_RECIPIENTS = None

    NOTIFICATION_EMAIL_TEMPLATE_NAME = (
            r'registration/notification_email.txt')
    NOTIFICATION_EMAIL_SUBJECT_TEMPLATE_NAME = (
            r'registration/notification_email_subject.txt')

    class Meta:
        prefix = 'registration'
