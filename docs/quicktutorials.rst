****************************
 Quick Tutorial
****************************


1. Install django-inspectional-registration
======================================================================================

django-inspectional-registration is found on PyPI so execute the
following command::

    $ pip install django-inspectional-registration

    or

    $ easy_install django-inspectional-registration

And also the application is developped on `github <https://github.com/lambdalisue/django-inspectional-registration>`_ so you
can install it from the repository as::

    $ pip install git+https://github.com/lambdalisue/django-inspectional-registration.git#egg=django-inspectional-registration

2.  Configure the application
==========================================================

To configure django-inspectional-registration, follow the instructions below

1.  Add ``'registration'``, ``'django.contrib.admin'`` to your ``INSTALLED_APPS`` of ``settings.py``

    .. Note::
        If you already use django-registration, see :doc:`quickmigrations` for
        migration.

2.  Add ``'registration.supplements.default'`` to your ``INSTALLED_APPS`` of
    ``settings.py`` or set ``REGISTRATION_SUPPLEMENT_CLASS`` to ``None``
    
    .. Note::
        django-inspectional-registration can handle registration supplemental
        information. If you want to use your own custom registration
        supplemental information, check :doc:`about_registration_supplement` for
        documents.

        Settings ``REGISTRATION_SUPPLEMENT_CLASS`` to ``None`` mean no
        registration supplemental information will be used.

3.  Add ``url('^registration/', include('registration.urls')),`` to your
    very top of (same directory as ``settings.py`` in default) ``urls.py`` like 
    below::

        from django.conf.urls.defaults import patterns, include, urls

        from django.contrib import admin
        admin.autodiscover()

        urlpatterns = pattern('',
            # some urls...

            # django-inspectional-registration require Django Admin page
            # to inspect registrations
            url('^admin/', include(admin.site.urls)),

            # Add django-inspectional-registration urls. The urls also define
            # Login, Logout and password_change or lot more for handle
            # registration.
            url('^registration/', include('registration.urls')),
        )

4.  Call ``syncdb`` command to create the database tables like below::

        $ ./manage.py syncdb

5.  Confirm that Django E-mail settings were properly configured. See
    https://docs.djangoproject.com/en/dev/topics/email/ for more detail.

    .. Note::
        If you don't want or too lazy to configure the settings. See
        `django-mailer <http://code.google.com/p/django-mailer/>`_ which store
        the email on database before sending.

        To use django-mailer insted of django's default email system in this
        application. Simply add 'mailer' to your ``INSTALLED_APPS`` then the
        application will use django-mailer insted.

How to use it
==========================

1.  Access http://localhost:8000/registration/register then you will see
    the registration page. So fill up (use your own real email address) the 
    fields and click ``Register`` button.

    .. Note::
        Did you start your development server? If not::

            $ ./manage.py runserver 8000

2.  Now go on the http://localhost:8000/admin/registration/registrationprofile/1/ 
    and accept your registration by clicking ``Save`` button.

    .. Note::
        To reject or force to activate the registration, change ``Action``
        and click ``Save``

        ``Message`` will be passed to each email template thus you can use the
        value of ``Message`` as ``{{ message }}`` in your email template. In
        default, the ``Message`` is only available in rejection email template
        to explain why the registration was rejected.

3.  You may get an Email from your website. The email contains an activation
    key so click the url.

    .. Note::
        If you get ``http://example.com/register/activate/XXXXXXXX`` for your
        activation key, that mean you haven't configure the site domain name
        in Django Admin. To prevent this, just set domain name of your site in
        Admin page.

4.  Two password form will be displayed on the activation page, fill up the
    password and click ``Activate`` to activate your account.


