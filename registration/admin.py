from django.contrib import admin
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from models import RegistrationProfile


class RegistrationAdmin(admin.ModelAdmin):
    actions = ['accept_users', 'reject_users', 'activate_users', 'resend_activation_email']
    list_display = ('user', 'get_status_display', 'activation_key_expired')
    raw_id_fields = ['user']
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    date_hierarchy = 'user__date_joined'
    list_filter = ('status', 'activation_key_expired')
    # User should not change status without Backend
    readonly_fields = ('_status')

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


admin.site.register(RegistrationProfile, RegistrationAdmin)
