#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
"""
A forms used in RegistrationAdmin


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
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from ..backends import get_backend
from ..models import RegistrationProfile

class RegistrationAdminForm(forms.ModelForm):
    """A special form for handling ``RegistrationProfile``

    This form handle ``RegistrationProfile`` correctly in ``save()``
    method. Because ``RegistrationProfile`` is not assumed to handle
    by hands, instance modification by hands is not allowed. Thus subclasses 
    should feel free to add any additions they need, but should avoid overriding 
    a ``save()`` method.

    """
    registration_backend = get_backend()

    UNTREATED_ACTIONS = (
            ('accept', _('Accept this registration')),
            ('reject', _('Reject this registration')),
            ('force_activate', _('Activate the associated user of this registration forcibly')),
        )
    ACCEPTED_ACTIONS = (
            ('activate', _('Activate the associated user of this registration')),
        )
    REJECTED_ACTIONS = (
            ('accept', _('Accept this registration')),
            ('force_activate', _('Activate the associated user of this registration forcibly')),
        )

    action = forms.ChoiceField(label=_('Action'))
    message = forms.CharField(label=_('Message'), 
            widget=forms.Textarea, required=False,
            help_text=_(
                'You can use the value of this field in templates for acceptance, '
                'rejection and activation email with "{{ message }}". It is displayed '
                'in rejection email as "Rejection reasons" in default templates.'
            ))

    class Meta:
        model = RegistrationProfile
        excludes = ('user', '_status')

    def __init__(self, *args, **kwargs):
        super(RegistrationAdminForm, self).__init__(*args, **kwargs)
        # dynamically set choices of _status field
        if self.instance._status == 'untreated':
            self.fields['action'].choices = self.UNTREATED_ACTIONS
        elif self.instance._status == 'accepted':
            self.fields['action'].choices = self.ACCEPTED_ACTIONS
        elif self.instance._status == 'rejected':
            self.fields['action'].choices = self.REJECTED_ACTIONS

    def clean_action(self):
        """clean action value

        Insted of raising AttributeError, validate the current registration
        profile status and the requested action and then raise ValidationError

        """
        action = self.cleaned_data['action']
        if action == 'accept':
            if self.instance._status == 'accepted':
                raise ValidationError(_("You cannot accept the registration which was accepted already."))
        elif action == 'reject':
            if self.instance._status == 'accepted':
                raise ValidationError(_("You cannot reject the registration which was accepted already."))
        elif action == 'activate':
            if self.instance._status != 'accepted':
                raise ValidationError(_("You cannot activate the user whom registration was not accepted yet."))
        elif action != 'force_activate':
            # with using django admin page, the code below never be called.
            raise ValidationError("Unknown action '%s' was requested." % action)
        return self.cleaned_data['action']

    def save(self, commit=True):
        """Call appropriate action via current registration backend

        Insted of modifing the registration profile, this method call current
        registration backend's accept/reject/activate method as requested.

        """
        fail_message = 'update' if self.instance.pk else 'create'
        opts = self.instance._meta
        if self.errors:
            raise ValueError("The %s chould not be %s because the data did'nt"
                             "validate." % (opts.object_name, fail_message))
        action = self.cleaned_data['action']
        message = self.cleaned_data['message']
        # this is a bit hack. to get request instance in form instance,
        # RegistrationAdmin save its request to bundle model instance
        _request = getattr(self.instance, settings._REGISTRATION_ADMIN_REQUEST_ATTRIBUTE_NAME_IN_MODEL_INSTANCE)
        if action == 'accept':
            self.registration_backend.accept(self.instance, _request, message=message)
        elif action == 'reject':
            self.registration_backend.reject(self.instance, _request, message=message)
        elif action == 'activate':
            # DO NOT delete profile otherwise Django Admin will raise IndexError
            self.registration_backend.activate(
                    self.instance.activation_key, _request, message=message,
                    no_profile_delete=True,
                )
        elif action == 'force_activate':
            self.registration_backend.accept(self.instance, _request, send_email=False)
            # DO NOT delete profile otherwise Django Admin will raise IndexError
            self.registration_backend.activate(
                    self.instance.activation_key, _request, message=message,
                    no_profile_delete=True,
                )
        else:
            raise AttributeError('Unknwon action "%s" was requested.' % action)
        if action not in ('activate', 'force_activate'):
            new_instance = self.instance.__class__.objects.get(pk=self.instance.pk)
        else:
            new_instance = self.instance
            # the instance has been deleted by activate method however
            # ``save()`` method will be called, thus set mock save method
            new_instance.save = lambda *args, **kwargs: new_instance
        return new_instance

    # this form doesn't have ``save_m2m()`` method and it is required
    # in default ModelAdmin class to use. thus set mock save_m2m method
    save_m2m = lambda x: x
