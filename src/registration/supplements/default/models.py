# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
A simple registration supplement model which requires ``remarks``
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.db import models
from django.utils.text import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from registration.supplements.base import RegistrationSupplementBase


@python_2_unicode_compatible
class DefaultRegistrationSupplement(RegistrationSupplementBase):
    """A simple registration supplement model which requires remarks"""
    remarks = models.TextField(_('remarks'))

    def __str__(self):
        """return a summary of this addition"""
        return self.remarks

    # it is required to specify from django 1.6
    class Meta:
        app_label = 'registration'
