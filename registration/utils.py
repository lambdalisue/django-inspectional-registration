#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Utilities


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
import re
import random

from django.utils.hashcompat import sha_constructor

def generate_activation_key(username):
    """generate activation key with username"""
    if isinstance(username, unicode):
        username = username.encode('utf-8')
    salt = sha_constructor(str(random.random())).hexdigest()[:5]
    activation_key = sha_constructor(salt+username).hexdigest()
    return activation_key

def generate_random_password(length=10):
    """generate random password"""
    # Without 1, l, O, 0 because those character are hard to tell
    # the difference between in same fonts
    chars = '23456789abcdefghijklmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
    password = "".join([random.choice(chars) for i in xrange(length)])
    return password



