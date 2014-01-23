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
from django.contrib.auth import views as auth_views
urlpatterns += patterns('',
    url(r'^login/$', auth_views.login,
        {'template_name': 'registration/login.html'},
        name='auth_login'),
    url(r'^logout/$', auth_views.logout,
        {'template_name': 'registration/logout.html'},
        name='auth_logout'),
    url(r'^password/change/$', auth_views.password_change,
        name='auth_password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done,
        name='auth_password_change_done'),
    url(r'^password/reset/$', auth_views.password_reset,
        name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete,
        name='auth_password_reset_complete'),
    url(r'^password/reset/done/$', auth_views.password_reset_done,
        name='auth_password_reset_done'),
)
