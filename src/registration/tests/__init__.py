import django

if django.VERSION < (1, 6):
    from test_admin import *
    from test_models import *
    from test_forms import *
    from test_views import *
    from test_backends import *
    from test_supplements import *

