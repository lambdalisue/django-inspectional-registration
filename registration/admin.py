from django.core.urlresolvers import reverse
from django.contrib import admin
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from models import RegistrationProfile


class RegistrationAdmin(admin.ModelAdmin):
    actions = ('accept_users', 'reject_users', 'activate_users', 'resend_activation_email')
    list_display = ('user', 'get_status_display', 'activation_key_expired') #, 'display_activation_key')
    raw_id_fields = ['user']
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_filter = ('_status', )
    # User should not change status without Backend
    readonly_fields = ('_status', )

    def get_actions(self, request):
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
        """
        Accept the selected users, if they are not alrady
        accepted.
        
        """
        for profile in queryset:
            RegistrationProfile.objects.accept_registration(profile)
    accept_users.short_description = _("Accept users")

    def reject_users(self, request, queryset):
        """
        Reject the selected users, if they are not alrady
        accepted.
        
        """
        for profile in queryset:
            RegistrationProfile.objects.reject_registration(profile)
    reject_users.short_description = _("Reject users")

    def activate_users(self, request, queryset):
        """
        Activates the selected users, if they are not alrady
        activated.
        
        """
        for profile in queryset:
            RegistrationProfile.objects.accept_registration(profile, send_email=False)
            RegistrationProfile.objects.activate_user(profile.activation_key)
    activate_users.short_description = _("Activate users")

    def resend_activation_email(self, request, queryset):
        """
        Re-sends activation emails for the selected users.

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
        if obj.status == 'accepted':
            activation_url = reverse('registration_activate', kwargs={'activation_key': obj.activation_key})
            return mark_safe(u"""<a href="%s">%s</a>""" % (activation_url, obj.activation_key))
        return 'Not available'
    display_activation_key.short_description = _('Activation key')
    display_activation_key.allow_tags = True





admin.site.register(RegistrationProfile, RegistrationAdmin)
