# coding=utf-8
"""
URLconf for django-inspectional-registration
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from registration.compat import url
from registration.compat import patterns

from registration.views import RegistrationView
from registration.views import RegistrationClosedView
from registration.views import RegistrationCompleteView
from registration.views import ActivationView
from registration.views import ActivationCompleteView

urlpatterns = patterns('',
    url(r'^activate/complete/$', ActivationCompleteView.as_view(),
        name='registration_activation_complete'),
    url(r'^activate/(?P<activation_key>\w+)/$', ActivationView.as_view(),
        name='registration_activate'),
    url(r'^register/$', RegistrationView.as_view(),
        name='registration_register'),
    url(r'^register/closed/$', RegistrationClosedView.as_view(),
        name='registration_disallowed'),
    url(r'^register/complete/$', RegistrationCompleteView.as_view(),
        name='registration_complete'),
)

# django.contrib.auth
from registration.conf import settings
from django.contrib.auth import views as auth_views
if settings.REGISTRATION_DJANGO_AUTH_URLS_ENABLE:
    prefix = settings.REGISTRATION_DJANGO_AUTH_URL_NAMES_PREFIX
    suffix = settings.REGISTRATION_DJANGO_AUTH_URL_NAMES_SUFFIX
    urlpatterns += patterns('',
        url(r'^login/$', auth_views.login,
            {'template_name': 'registration/login.html'},
            name=prefix+'login'+suffix),
        url(r'^logout/$', auth_views.logout,
            {'template_name': 'registration/logout.html'},
            name=prefix+'logout'+suffix),
        url(r'^password/change/$', auth_views.password_change,
            name=prefix+'password_change'+suffix),
        url(r'^password/change/done/$', auth_views.password_change_done,
            name=prefix+'password_change_done'+suffix),
        url(r'^password/reset/$', auth_views.password_reset,
            name=prefix+'password_reset'+suffix, kwargs=dict(
                post_reset_redirect=prefix+'password_reset_done'+suffix)),
        url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
            auth_views.password_reset_confirm,
            name=prefix+'password_reset_confirm'+suffix),
        url(r'^password/reset/complete/$', auth_views.password_reset_complete,
            name=prefix+'password_reset_complete'+suffix),
        url(r'^password/reset/done/$', auth_views.password_reset_done,
            name=prefix+'password_reset_done'+suffix),
    )
