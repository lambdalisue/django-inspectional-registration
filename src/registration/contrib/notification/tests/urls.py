from registration.compat import url
from registration.compat import patterns
from registration.compat import include

from django.contrib import admin
admin.autodiscover()

# default template used in template
# require admin site
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)
