from django.conf import settings
#from django.core.exceptions import ImproperlyConfigured

#def checkconf(name, msg):
#    """check django.conf.settings is proprely configured"""
#    if not hasattr(settings, name):
#        raise ImproperlyConfigured(msg)

def setconf(name, default_value):
    """set default value to django.conf.settings"""
    value = getattr(settings, name, default_value)
    setattr(settings, name, value)

setconf('ACCOUNT_ACTIVATION_DAYS', 7)
setconf('REGISTRATION_DEFAULT_PASSWORD_LENGTH', 10)
setconf('REGISTRATION_BACKEND_CLASS', 'registration.backends.default.DefaultRegistrationBackend')
#setconf('REGISTRATION_SUPPLEMENT_CLASS', 'registration.supplements.default.DefaultRegistrationSupplement')
setconf('REGISTRATION_SUPPLEMENT_CLASS', None)
setconf('REGISTRATION_SUPPLEMENT_ADMIN_INLINE_BASE_CLASS', 'registration.admin.RegistrationSupplementAdminInlineBase')
setconf('REGISTRATION_OPEN', True)

setconf('REGISTRATION_REGISTRATION_EMAIL', True)
setconf('REGISTRATION_ACCEPTANCE_EMAIL', True)
setconf('REGISTRATION_REJECTION_EMAIL', True)
setconf('REGISTRATION_ACTIVATION_EMAIL', True)

setconf('_REGISTRATION_ADMIN_REQUEST_ATTRIBUTE_NAME_IN_MODEL_INSTANCE', '_registration_admin_request')
