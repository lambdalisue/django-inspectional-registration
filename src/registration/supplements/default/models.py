# coding=utf-8
"""
A simple registration supplement model which requires ``remarks``
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.db import models
from django.utils.text import ugettext_lazy as _
from registration.supplements import RegistrationSupplementBase


class DefaultRegistrationSupplement(RegistrationSupplementBase):
    """A simple registration supplement model which requires remarks"""
    remarks = models.TextField(_('remarks'))

    def __unicode__(self):
        """return a summary of this addition"""
        return self.remarks

    # it is required to specify from django 1.6
    class Meta:
        app_label = 'registration'
