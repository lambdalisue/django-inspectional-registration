********************************
 Quick Migrations
********************************

Instructions
========================

django-inspectional-registration can be migrate from django-registration by
south. To migrate, follow the instructions

1.  Confirm your application has ``'south'``, ``'django.contrib.admin'`` and
    in your ``INSTALLED_APPS``, if you haven't, 
    add these and run ``syncdb`` command to create the database table required.

2.  Execute following commands::

        $ ./manage.py migrate registration 0001 --fake
        $ ./manage.py migrate registration

3.  Rewrite your most top of ``urls.py`` as::

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

4.  Set ``REGISTRATION_SUPPLEMENT_CLASS`` to ``None`` in your ``settings.py``

    .. Note::
        django-inspectional-registration can handle registration supplemental
        information. If you want to use your own custom registration
        supplemental information, check :doc:`about_registration_supplement` for
        documents.

        Settings ``REGISTRATION_SUPPLEMENT_CLASS`` to ``None`` mean no
        registration supplemental information will be used.
        
5.  Done. Enjoy!

The database difference between django-registration and django-inspectional-registration
================================================================================================================================================================================

django-inspectional-registration add new ``CharField`` named :py:attr:`registration.models.RegistrationProfile._status` to
the :py:class:`registration.models.RegistrationProfile` and change the storategy to delete
``RegistrationProfile`` which has been activated from the database insted of
setting ``'ALREADY_ACTIVATED'`` to :py:attr:`registration.models.RegistrationProfile.activation_key`.

``activation_key`` will be generated when the ``_status`` of ``RegistrationProfile``
be ``'accepted'`` otherwise it is set ``None``

