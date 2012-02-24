#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
A simple registration supplement model which requires ``remarks``


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
from django.db import models
from django.utils.text import ugettext_lazy as _

from registration.supplements import RegistrationSupplementBase

class DefaultRegistrationSupplement(RegistrationSupplementBase):
    """A simple registration supplement model which requires remarks"""
    remarks = models.TextField(_('remarks'))

    def __unicode__(self):
        """return a summary of this addition"""
        return self.remarks
