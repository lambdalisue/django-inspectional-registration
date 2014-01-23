# coding=utf-8
"""
Django custom signals used in django-inspectional-registration

SIGNALS:
    user_registered
        sent when user has registered by Backend

    user_accepted
        sent when user registration has accepted by Backend

    user_rejected
        sent when user registration has rejected by Backend

    user_activated
        sent when user has activated by Backend
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
__all__ = (
    'user_registered', 'user_accepted',
    'user_rejected', 'user_activated'
)
from django.dispatch import Signal

# A new user has registered
user_registered = Signal(providing_args=['user', 'profile', 'request'])

# A user has been accepted his/her registration
user_accepted = Signal(providing_args=['user', 'profile', 'request'])

# A user has been rejected his/her registration
user_rejected = Signal(providing_args=['user', 'profile', 'request'])

# A user has activated his/her account.
user_activated = Signal(providing_args=['user', 'password', 'is_generated',
                                        'request'])
