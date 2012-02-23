#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Forms of django-inspection

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
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

attrs_dict = {'class': 'required'}

class ActivationForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password (again)"))
    
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data

class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})
    email1 = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)),
                             label=_("E-mail"))
    email2 = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)),
                             label=_("E-mail (again)"))

    def clean_username(self):
        try:
            User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean(self):
        if 'email1' in self.cleaned_data and 'email2' in self.cleaned_data:
            if self.cleaned_data['email1'] != self.cleaned_data['email2']:
                raise forms.ValidationError(_("The two email fields didn't match."))
        return self.cleaned_data

class RegistrationFormTermsOfService(RegistrationForm):
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
                             label=_(u'I have read and agree to the Terms of Service'),
                             error_messages={'required': _("You must agree to the terms to register")})

class RegistrationFormUniqueEmail(RegistrationForm):
    def clean_email1(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email1']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email1']


class RegistrationFormNoFreeEmail(RegistrationForm):
    bad_domains = ['aim.com', 'aol.com', 'email.com', 'gmail.com',
                   'googlemail.com', 'hotmail.com', 'hushmail.com',
                   'msn.com', 'mail.ru', 'mailinator.com', 'live.com',
                   'yahoo.com']
    
    def clean_email1(self):
        email_domain = self.cleaned_data['email1'].split('@')[1]
        if email_domain in self.bad_domains:
            raise forms.ValidationError(_("Registration using free email addresses is prohibited. Please supply a different email address."))
        return self.cleaned_data['email1']
