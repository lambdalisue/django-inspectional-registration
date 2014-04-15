django-inspectional-registration
===============================================================================
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

-   Can be migrated from django-registration_ simply by south_

-   `django-mailer <http://code.google.com/p/django-mailer/>`_ compatible.
    Emails sent from the application will use django-mailer if 'mailer' is
    in your ``INSTALLED_APPS``

The difference with django-registration
------------------------------------------------------------------------------

While django-registration_ requires 3 steps for registration,
django-inspectional-registration requires 5 steps and inspector for
registration.

.. _django-registration: https://bitbucket.org/ubernostrum/django-registration/
.. _south: http://south.aeracode.org/

Online documentation
-------------------------------------------------------------------------------
See `django-inspectional-registration official documents <http://readthedocs.org/docs/django-inspectional-registration/en/latest/>`_ for more detail
