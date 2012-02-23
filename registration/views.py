#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
short module explanation


AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__AUTHOR__ = "lambdalisue (lambdalisue@hashnote.net)"
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import ProcessFormView
from django.views.generic.edit import FormMixin
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import SingleObjectMixin
from django.utils.text import ugettext_lazy as _

from backends import get_backend
from models import RegistrationProfile


class RegistrationCompleteView(TemplateView):
    template_name = r'registration/registration_complete.html'

class RegistrationClosedView(TemplateView):
    template_name = r'registration/registration_closed.html'

class ActivationCompleteView(TemplateView):
    template_name = r'registration/activation_complete.html'

class ActivationView(SingleObjectMixin, FormMixin, TemplateResponseMixin, ProcessFormView):
    template_name = r'registration/activation_form.html'
    model = RegistrationProfile
    backend = get_backend()

    def get_queryset(self):
        return self.model.objects.filter(_status='accepted')

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()
        try:
            obj = queryset.get(activation_key=self.kwargs['activation_key'])
            if obj.activation_key_expired():
                raise Http404(_('The activation key has expired'))
        except self.model.DoesNotExist:
            raise Http404(_('An invalid activation key has passed'))
        return obj

    def get_success_url(self):
        return self.backend.get_activation_complete_url(self.activated_user)

    def get_form_class(self):
        return self.backend.get_activation_form_class()

    def form_valid(self, form):
        profile = self.get_object()
        password = form.cleaned_data['password1']
        self.activated_user = self.backend.activate(profile.activation_key, password)
        return super(ActivationView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ActivationView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ActivationView, self).post(request, *args, **kwargs)

class RegistrationView(FormMixin, TemplateResponseMixin, ProcessFormView):
    template_name = r'registration/registration_form.html'
    backend = get_backend()

    def get_success_url(self):
        return self.backend.get_registration_complete_url(self.new_user)

    def get_disallowed_url(self):
        return self.backend.get_registration_closed_url()

    def get_form_class(self):
        return self.backend.get_registration_form_class()

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email1']
        self.new_user = self.backend.register(username, email)
        return super(RegistrationView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not self.backend.registration_allowed():
            return redirect(self.get_disallowed_url())
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)
