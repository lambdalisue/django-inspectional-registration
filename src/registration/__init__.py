# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from app_version import get_versions
__version__, VERSION = get_versions('django-inspectional-registration',
                                    allow_ambiguous=True)
