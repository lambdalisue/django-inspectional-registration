# -*- coding: utf-8 -*-
from __future__ import unicode_literals
try:
    from django.conf.urls import url, patterns, include
except ImportError:
    from django.conf.urls.defaults import url, patterns, include
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^registration/', include('registration.urls')),
)
