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


How can I get notification email when new user has registered in the site?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use :mod:`registration.contrib.notification`.

Add ``'registration.contrib.notification'`` to your ``INSTALLED_APPS`` and create
following template files in your template directory.

-   ``registration/notification_email.txt``
-   ``registration/notification_email_subject.txt``


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
        from registration.signals import user_registered

        def automatically_accept_registration_reciver(sender, user, profile, request, **kwargs):
            backend = get_backend()
            backend.accept(profile, request=request)
        user_registered.connect(automatically_accept_registration_reciver)

Then the application behaviors like django-registration_
            

How can I contribute to django-inspectional-registration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Any contributions include `adding translations <https://docs.djangoproject.com/en/1.3/topics/i18n/localization/>`_ are welcome! 
Use github's ``pull request`` for contribution.

.. _django-registration: https://bitbucket.org/ubernostrum/django-registration/

