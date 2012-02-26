#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
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
from django.dispatch import Signal

# A new user has registered
user_registered = Signal(providing_args=['user', 'profile', 'request'])

# A user has been accepted his/her registration
user_accepted = Signal(providing_args=['user', 'profile', 'request'])

# A user has been rejected his/her registration
user_rejected = Signal(providing_args=['user', 'profile', 'request'])

# A user has activated his/her account.
user_activated = Signal(providing_args=['user', 'password', 'is_generated', 'request'])
