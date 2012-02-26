django-inspectional-registration is a enhanced application of
django-registration_. The following features are available

-   Inspection steps for registration. You can accept or reject the account
    registration before sending activation key to the user.

-   Password will be filled in after the activation step to prevent that the
    user forget them previously filled password in registration step (No
    password filling in registration step)

-   Password can be generated programatically and force to activate the
    user. The generated password will be sent to the user by e-mail.

-   Any Django models are available to use as supplemental information of
    registration if the models are subclasses of
    ``registration.supplements.RegistrationSupplementBase``. 
    It is commonly used for inspection.

-   You can send any additional messages to the user in each steps
    (acception, rejection and activation)

-   The behaviors of the application are customizable with Backend feature.

-   The E-mails or HTMLs are customizable with Django template system.

-   Can be migrate from django-registration_ simply by south_

-   `django-mailer <http://code.google.com/p/django-mailer/>`_ compatible.
    Emails sent from the application will use django-mailer if 'mailer' is
    in your ``INSTALLED_APPS``

See `django-inspectional-registration official documents <http://readthedocs.org/docs/django-inspectional-registration/en/latest/>`_ for more detail

The difference between django-registration
------------------------------------------------------------------------------------

While django-registration_ requires 3 steps for registration,
django-inspectional-registration requires 5 steps and inspector for
registration.

.. _django-registration: https://bitbucket.org/ubernostrum/django-registration/
.. _south: http://south.aeracode.org/

FAQ
------

Help! Email have not been sent to the user!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To enable sending email in django, you must have the following settings in your
``settings.py``::

    # if your smtp host use TLS
    #EMAIL_USE_TLS = True
    # url of your smtp host
    EMAIL_HOST = ''
    # if your smtp host requre username
    #EMAIL_HOST_USER = ''
    # if your smtp host require password
    #EMAIL_HOST_PASSWORD = ''
    # port number which your smtp host used (default 25)
    # EMAIL_PORT = 587
    DEFAULT_FROM_EMAIL = 'webmaster@your.domain'

If you don't have SMTP host but you have Gmail, use the following settings
to use your Gmail for SMTP host::

    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'your_email_address@gmail.com'
    EMAIL_HOST_PASSWORD = 'your gmail password'
    DEFAULT_FROM_EMAIL = 'your_email_address@gmail.com'


I want to use django-inspectional-registration but I don't need inspection step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you don't need inspection step, use original django-registration_ in that
case.

However, sometime you do may want to use django-inspectional-registration but
inspection. Then follow the instructions below

1.  Disable sending registration email with setting
    ``REGISTRATION_REGISTRATION_EMAIL`` to ``False``

2.  Add special signal reciever which automatically accept the user
    registration::

        from registration.backends import get_backend
        from registration.signals import user_accepted

        def automatically_accept_registration_reciver(sender, user, profile, request, **kwargs):
            backend = get_backend()
            backend.accept(profile, request=request)
        user_accepted.connect(automatically_accept_registration_reciver)

Then the application behaviors like django-registration_
            

How can I contribute to django-inspectional-registration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Any contributions include `adding translations <https://docs.djangoproject.com/en/1.3/topics/i18n/localization/>`_ are welcome! 
Use github's ``pull request`` for contribution.

