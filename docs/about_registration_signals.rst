******************************************************
 About Registration Signals
******************************************************
django-inspectional-registration provide the following signals.

``user_registered(user, profile, request)``
    It is called when a user has registered.
    The arguments are:

    ``user``
        An instance of User model
    ``profile``
        An instance of RegistrationProfile model of the ``user``
    ``request``
        An instance of django's HttpRequest. It is useful to automatically get
        extra user informations

``user_accepted(user, profile, request)``
    It is called when a user has accepted by inspectors.
    The arguments are:

    ``user``
        An instance of User model
    ``profile``
        An instance of RegistrationProfile model of the ``user``
    ``request``
        An instance of django's HttpRequest. It is useful to automatically get
        extra user informations

``user_rejected(user, profile, request)``
    It is called when a user has rejected by inspectors.
    The arguments are:

    ``user``
        An instance of User model
    ``profile``
        An instance of RegistrationProfile model of the ``user``
    ``request``
        An instance of django's HttpRequest. It is useful to automatically get
        extra user informations

``user_activated(user, profile, is_generated, request)``
    It is called when a user has activated by 1) the user access the activation
    url, 2) inspectors forcely activate the user.
    The arguments are:

    ``user``
        An instance of User model
    ``password``
        If the user have forcely activated by inspectors, this indicate the
        raw password, otherwise it is ``None`` (So that non automatically
        generated user password is protected from the suffering).
    ``is_generated``
        When inspectors forcely activate the user, it become ``True``.
        It mean that the user do not know own account password thus you need to
        tell the password to the user somehow (default activation e-mail
        automatically include the user password if this ``is_generated`` is
        ``True``)
    ``request``
        An instance of django's HttpRequest. It is useful to automatically get
        extra user informations

