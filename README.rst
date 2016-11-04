django-inspectional-registration
===============================================================================
.. image:: https://secure.travis-ci.org/lambdalisue/django-inspectional-registration.png?branch=master
    :target: http://travis-ci.org/lambdalisue/django-inspectional-registration
    :alt: Build status

.. image:: https://coveralls.io/repos/lambdalisue/django-inspectional-registration/badge.png?branch=master
    :target: https://coveralls.io/r/lambdalisue/django-inspectional-registration/
    :alt: Coverage

.. image:: https://requires.io/github/lambdalisue/django-inspectional-registration/requirements.svg?branch=master
    :target: https://requires.io/github/lambdalisue/django-inspectional-registration/requirements/?branch=master
    :alt: Requirements Status

.. image:: https://landscape.io/github/lambdalisue/django-inspectional-registration/master/landscape.svg?style=flat
   :target: https://landscape.io/github/lambdalisue/django-inspectional-registration/master
   :alt: Code Health

.. image:: https://scrutinizer-ci.com/g/lambdalisue/django-inspectional-registration/badges/quality-score.png?b=master
    :target: https://scrutinizer-ci.com/g/lambdalisue/django-inspectional-registration/inspections
    :alt: Inspection


Author
    Alisue <lambdalisue@hashnote.net>
Supported python versions
    2.6, 2.7, 3.2, 3.3, 3.4, 3.5
Supported django versions
    1.5 - 1.10

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


For translators
---------------------------------------------------------------------------------
To create a message file, execute the following command (with your language)

.. code:: sh

    $ python manage.py makemessages -l ja


You can compile the latest message files with the following command

.. code:: sh

    $ python setup.py compile_messages

The command above is automatically called before ``sdist`` command if you call
``python manage.py sdist``.

Email
---------------------------------------------------------------------------------
REGISTRATION_FROM_EMAIL is used as the *FROM* email address emails send by 
django-inspectional-registration. If REGISTRATION_FROM_EMAIL is not set the Django 
setting _DEFAULT_FROM_EMAIL: <https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email/> 
will be used instead.

To set REGISTRATION_FROM_EMAIL add REGISTRATION_FROM_EMAIL to your settings file.

Example:

``REGISTRATION_FROM_EMAIL = 'help@example.com'``

Backward incompatibility
---------------------------------------------------------------------------------
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

Because of an `issue#36 <https://github.com/lambdalisue/django-inspectional-registration/issues/36>`_, django-inspectional-registration add the following new option.

-   ``REGISTRATION_USE_OBJECT_PERMISSION``
    If it is ``True``, django-inspectional-registration pass ``obj`` to ``request.user.has_perm`` in ``RegistrationAdmin.has_*_permission()`` methods. A default permission backend of Django does not support object permission thus it should be ``False`` if you don't use extra permission backends such as `django-permission <https://lambdalisue/django-permission>`_.

This change was introduced from version 0.4.7. To keep backward compatibility, write the following in your settings module.

.. code:: python

    REGISTRATION_USE_OBJECT_PERMISSION = True
