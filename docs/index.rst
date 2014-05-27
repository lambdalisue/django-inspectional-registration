************************************************************
Welcome to django-inspectional-registration's documentation!
************************************************************
.. image:: https://secure.travis-ci.org/lambdalisue/django-inspectional-registration.png?branch=master
    :target: http://travis-ci.org/lambdalisue/django-inspectional-registration
    :alt: Build status

.. image:: https://coveralls.io/repos/lambdalisue/django-inspectional-registration/badge.png?branch=master
    :target: https://coveralls.io/r/lambdalisue/django-inspectional-registration/
    :alt: Coverage

.. image:: https://pypip.in/d/django-inspectional-registration/badge.png
    :target: https://pypi.python.org/pypi/django-inspectional-registration/
    :alt: Downloads

.. image:: https://pypip.in/v/django-inspectional-registration/badge.png
    :target: https://pypi.python.org/pypi/django-inspectional-registration/
    :alt: Latest version

.. image:: https://pypip.in/wheel/django-inspectional-registration/badge.png
    :target: https://pypi.python.org/pypi/django-inspectional-registration/
    :alt: Wheel Status

.. image:: https://pypip.in/egg/django-inspectional-registration/badge.png
    :target: https://pypi.python.org/pypi/django-inspectional-registration/
    :alt: Egg Status

.. image:: https://pypip.in/license/django-inspectional-registration/badge.png
    :target: https://pypi.python.org/pypi/django-inspectional-registration/
    :alt: License

Author
    Alisue <lambdalisue@hashnote.net>
Supported python versions
    2.6, 2.7, 3.2, 3.3
Supported django versions
    1.3 - 1.6

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
    (acceptance, rejection and activation)

-   The behaviors of the application are customizable with Backend feature.

-   The E-mails or HTMLs are customizable with Django template system.

-   Can be migrate from django-registration_ simply by south_

-   `django-mailer <http://code.google.com/p/django-mailer/>`_ compatible.
    Emails sent from the application will use django-mailer if 'mailer' is
    in your ``INSTALLED_APPS``


Documentations
==============================================================================

.. toctree::
    :maxdepth: 2

    quicktutorials
    quickmigrations
    about_registration_supplement
    about_registration_backend
    about_registration_templates
    about_registration_signals
    about_registration_settings
    about_registration_contrib
    faq

    API Reference <modules>

The difference between django-registration
==============================================================================

While django-registration_ requires 3 steps for registration,
django-inspectional-registration requires 5 steps and inspector for
registration. See the conceptual summary below.


.. image:: _static/img/difference_summary.png


.. _django-registration: https://bitbucket.org/ubernostrum/django-registration/
.. _south: http://south.aeracode.org/


For translators
================================================================================
You can compile the latest message files with the following command

.. code:: sh

    $ python setup.py compile_messages

The command above is automatically called before ``sdist`` command if you call
``python manage.py sdist``.


Backward incompatibility
================================================================================
Because of an `issue#24 <https://github.com/lambdalisue/django-inspectional-registration/issues/24>`_, django-inspectional-registration add the following three new options.

-   ``REGISTRATION_DJANGO_AUTH_URLS_ENABLE``
    If it is ``False``, django-inspectional-registration do not define the views of django.contrib.auth.
    It is required to define these view manually. (Default: ``True``)
-   ``REGISTRATION_DJANGO_AUTH_URL_NAMES_PREFIX``
    It is used as a prefix string of view names of django.contrib.auth.
    For backward compatibility, set this value to ``'auth_'``. (Default: ``''``)
-   ``REGISTRATION_DJANGO_AUTH_URL_NAMES_SUFFIX``
    It is used as a suffix string of view names of django.contrib.auth.
    For backward compatibility, set this value to ``''``. (Default: ``''``)

This changes were introduced from version 0.4.0, to keep the backward compatibility, write the following in your settings module.

.. code:: python

    REGISTRATION_DJANGO_AUTH_URLS_ENABLE = True
    REGISTRATION_DJANGO_AUTH_URL_NAMES_PREFIX = 'auth_'
    REGISTRATION_DJANGO_AUTH_URL_NAMES_SUFFIX = ''


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

