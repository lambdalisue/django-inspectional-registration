# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from registration.compat import url, patterns, include
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^registration/', include('registration.urls')),
)
