#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Admins of django-inspectional-registration

This is a modification of django-registration_ ``admin.py``
The original code is written by James Bennett

.. _django-registration: https://bitbucket.org/ubernostrum/django-registration


CLASSES:
    ActivationForm                  -- Form for activation
    RegistrationForm                -- Form for registration
    RegistrationFormTermOfService   -- ``RegistrationForm`` with agreement to
                                       a site's Terms of Services
    RegistrationFormUniqueEmail     -- ``RegistrationForm`` which enforce
                                       uniqueness of email addresses
    RegistrationFormNoFreeEmail     -- ``RegistrationForm`` which disallows
                                       registration with email addresses from
                                       popular free webmail services

AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

Original License:
    Copyright (c) 2007-2011, James Bennett
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are
    met:

        * Redistributions of source code must retain the above copyright
        notice, this list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above
        copyright notice, this list of conditions and the following
        disclaimer in the documentation and/or other materials provided
        with the distribution.
        * Neither the name of the author nor the names of other
        contributors may be used to endorse or promote products derived
        from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
    A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
    OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from models import RegistrationProfile

class RegistrationAdmin(admin.ModelAdmin):
    """An admin model of RegistrationProfile"""
    actions = ('accept_users', 'reject_users', 'activate_users', 'resend_activation_email')
    list_display = ('user', 'get_status_display', 'activation_key_expired') #, 'display_activation_key')
    raw_id_fields = ['user']
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_filter = ('_status', )
    # User should not change status without Backend
    readonly_fields = ('_status', )

    def get_actions(self, request):
        """get actions displaied in admin site

        RegistrationProfile should not be deleted in admin site thus
        'delete_selected' is disabled in default.

        Each actions has permissions thus delete the action if the accessed
        user doesn't have appropriate permission.

        """
        actions = super(RegistrationAdmin, self).get_actions(request)
        try:
            del actions['delete_selected']
        except KeyError:
            pass
        if not request.user.has_perm('registration.accept_registration'):
            del actions['accept_users']
        if not request.user.has_perm('registration.reject_registration'):
            del actions['reject_users']
        if not request.user.has_perm('registration.activate_user'):
            del actions['activate_users']
        return actions
                                                                    
    def accept_users(self, request, queryset):
        """Accept the selected users, if they are not already accepted"""
        for profile in queryset:
            RegistrationProfile.objects.accept_registration(profile)
    accept_users.short_description = _("Accept users")

    def reject_users(self, request, queryset):
        """Reject the selected users, if they are not already accepted"""
        for profile in queryset:
            RegistrationProfile.objects.reject_registration(profile)
    reject_users.short_description = _("Reject users")

    def activate_users(self, request, queryset):
        """Activates the selected users, if they are not already activated"""
        for profile in queryset:
            RegistrationProfile.objects.accept_registration(profile, send_email=False)
            RegistrationProfile.objects.activate_user(profile.activation_key)
    activate_users.short_description = _("Activate users")

    def resend_activation_email(self, request, queryset):
        """Re-sends activation emails for the selected users

        Note that this will *only* send activation emails for users
        who are eligible to activate; emails will not be sent to users
        whose activation keys have expired or who have already
        activated.
        
        """
        for profile in queryset:
            if not profile.activation_key_expired():
                profile.send_activation_email()
    resend_activation_email.short_description = _("Re-send activation emails")

    def display_activation_key(self, obj):
        """Display activation key with link

        Note that displaying activation key is not recommended in security reason.
        If you really want to use this method, create your own subclass and
        re-register to admin.site

        Even this is a little bit risky, it is really useful for developping
        (without checking email, you can activate any user you want) thus 
        I created but turned off in default :-p

        """
        if obj.status == 'accepted':
            activation_url = reverse('registration_activate', kwargs={'activation_key': obj.activation_key})
            return mark_safe(u"""<a href="%s">%s</a>""" % (activation_url, obj.activation_key))
        return 'Not available'
    display_activation_key.short_description = _('Activation key')
    display_activation_key.allow_tags = True

admin.site.register(RegistrationProfile, RegistrationAdmin)
