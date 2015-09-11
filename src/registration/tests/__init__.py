# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django

if django.VERSION < (1, 6):
    from registration.tests.test_admin import *
    from registration.tests.test_models import *
    from registration.tests.test_forms import *
    from registration.tests.test_views import *
    from registration.tests.test_backends import *
    from registration.tests.test_supplements import *

