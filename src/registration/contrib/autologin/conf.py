# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.conf import settings
from appconf import AppConf


class InspectionalRegistrationAutoLoginAppConf(AppConf):
    AUTO_LOGIN = True

    class Meta:
        prefix = 'registration'
