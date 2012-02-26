********************************************************
 About Registration Templates
********************************************************

django-inspectional-registration use the following templates

Email templates
==============================
Used to create the email

acceptance Email
------------------------------
Sent when inspector accpet the account registration

``registration/acceptance_email.txt``
    Used to create acceptance email. The following context will be passed

    ``site``
        An instance of ``django.contrib.site.Site`` to determine the site name
        and domain name

    ``user``
        A user instance
    
    ``profile``
        An instance of :py:class:`registration.models.RegistrationProfile`

    ``activation_key``
        An activation key used to generate activation url. To generate
        activation url, use the following template command::

            {% load url from future %}
            
            http://{{ site.domain }}{% url 'registration_activate' activation_key=activation_key %}

    ``expiration_days``
        A number of days remaining during which the account may be activated.

    ``message``
        A message from inspector. Not used in default template.

``registration/acceptance_email_subject.txt``
    Used to create acceptance email subject. The following context will be passed

    ``site``
        An instance of ``django.contrib.site.Site`` to determine the site name
        and domain name

    ``user``
        A user instance
    
    ``profile``
        An instance of :py:class:`registration.models.RegistrationProfile`

    ``activation_key``
        An activation key used to generate activation url. To generate
        activation url, use the following template command::

            {% load url from future %}
            
            http://{{ site.domain }}{% url 'registration_activate' activation_key=activation_key %}

    ``expiration_days``
        A number of days remaining during which the account may be activated.

    ``message``
        A message from inspector. Not used in default template.

    .. Note::
        All newline will be removed in this template because it is a subject.

Activation Email
--------------------------------
Sent when the activation has complete.

``registration/activation_email.txt``
    Used to create activation email. The following context will be passed

    ``site``
        An instance of ``django.contrib.site.Site`` to determine the site name
        and domain name

    ``user``
        A user instance
    
    ``password``
        A password of the account. Use this for telling the password when the
        password is generated automatically.

    ``is_generated``
        If ``True``, the password was generated programatically thus you have
        to tell the password to the user.

    ``message``
        A message from inspector. Not used in default template.

``registration/activation_email_subject.txt``
    Used to create activation email subject. The following context will be passed

    ``site``
        An instance of ``django.contrib.site.Site`` to determine the site name
        and domain name

    ``user``
        A user instance
    
    ``password``
        A password of the account. Use this for telling the password when the
        password is generated automatically.

    ``is_generated``
        If ``True``, the password was generated programatically thus you have
        to tell the password to the user.

    ``message``
        A message from inspector. Not used in default template.

    .. Note::
        All newline will be removed in this template because it is a subject.

Registration Email
------------------------------------
Sent when the registration has complete.

``registration/registration_email.txt``
    Used to create registration email. The following context will be passed

    ``site``
        An instance of ``django.contrib.site.Site`` to determine the site name
        and domain name

    ``user``
        A user instance

    ``profile``
        An instance of :py:class:`registration.models.RegistrationProfile`

``registration/registration_email_subject.txt``
    Used to create registration email subject. The following context will be passed

    ``site``
        An instance of ``django.contrib.site.Site`` to determine the site name
        and domain name

    ``user``
        A user instance

    ``profile``
        An instance of :py:class:`registration.models.RegistrationProfile`

    .. Note::
        All newline will be removed in this template because it is a subject.

Rejection Email
------------------------------
Sent when inspector reject the account registration

``registration/rejection_email.txt``
    Used to create rejection email. The following context will be passed

    ``site``
        An instance of ``django.contrib.site.Site`` to determine the site name
        and domain name

    ``user``
        A user instance
    
    ``profile``
        An instance of :py:class:`registration.models.RegistrationProfile`

    ``message``
        A message from inspector. Used for explain why the account
        registration was rejected in default template

``registration/rejection_email_subject.txt``
    Used to create rejection email subject. The following context will be passed

    ``site``
        An instance of ``django.contrib.site.Site`` to determine the site name
        and domain name

    ``user``
        A user instance
    
    ``profile``
        An instance of :py:class:`registration.models.RegistrationProfile`

    ``message``
        A message from inspector. Used for explain why the account
        registration was rejected in default template

    .. Note::
        All newline will be removed in this template because it is a subject.

HTML Templates
============================
The following template will be used

``registration/activation_complete.html``
    Used for activation complete page.

``registration/activation_form``
    Used for activation page. ``form`` context will be passed
    to generate the activation form.

``registration/login.html``
    Used for login page. ``form`` context will be passed
    to generate the login form.

``registration/logout.html``
    Used for logged out page.

``registration/registration_closed.html``
    Used for registration closed page.

``registration/registration_complete.html``
    Used for registration complete page.

``registration/registration_form.html``
    Used for registration page. ``form`` context will be passed
    to generate registration form and ``supplement_form`` context
    will be passed to generate registration supplement form when
    the registration supplement exists. Use the following code
    in your template::

        <form action="" method="post">{% csrf_token %}
            {{ form.as_p }}
            {{ supplement_form.as_p }}
            <p><input type="submit" value="Register"></p>
        </form>

