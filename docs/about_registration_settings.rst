******************************************************
 About Registration Settings
******************************************************

``ACCOUNT_ACTIVATION_DAYS``
    The number of days to determine the remaining during which the account may
    be activated.

    Default: ``7``

``REGISTRATION_DEFAULT_PASSWORD_LENGTH``
    The integer length of the default password programatically generate.

    Default: ``10``

``REGISTRATION_BACKEND_CLASS``
    A string dotted python path for registration backend class.

    Default: ``'registration.backends.default.DefaultRegistrationBackend'``

``REGISTRATION_SUPPLEMENT_CLASS``
    A string dotted python path for registration supplement class.

    Default: ``'registration.supplements.default.DefaultRegistrationSupplement'``

``REGISTRATION_ADMIN_INLINE_BASE_CLASS``
    A string dotted python path for registration supplement admin inline base
    class.

    Default: ``'registration.admin.RegistrationSupplementAdminInlineBase'``

``REGISTRATION_OPEN``
    A boolean value whether the registration is currently allowed.

    Default: ``True``

``REGISTRATION_REGISTRATION_EMAIL``
    Set ``False`` to disable sending registration email to the user.

    Default: ``True``

``REGISTRATION_ACCEPTION_EMAIL``
    Set ``False`` to disable sending acception email to the user.

    Default: ``True``

``REGISTRATION_REJECTION_EMAIL``
    Set ``False`` to disable sending rejection email to the user.

    Default: ``True``

``REGISTRATION_ACTIVATION_EMAIL``
    Set ``False`` to disable sending activation email to the user.

    Default: ``True``

