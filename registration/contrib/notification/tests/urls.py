from django.conf.urls.defaults import patterns, include, url
from registration.tests.urls import urlpatterns

from django.contrib import admin
admin.autodiscover()

# default template used in template
# require admin site
urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)
