try:
    # django 1.4
    from django.conf.urls import url, patterns
except ImportError:
    from django.conf.urls.defaults import url, patterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^registration/', include('registration.urls')),
    url(r'^', include('miniblog.blogs.urls')),
)
