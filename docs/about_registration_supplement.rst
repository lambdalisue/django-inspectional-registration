**********************************************************
 About Registration Supplement
**********************************************************

Registration Supplement is a django model class which inherit
:py:class:`registration.supplements.RegistrationSupplementBase`.
It is used to add supplemental information to each registration.
Filling the supplemental information is required in registration step
and the filled supplemental information will be displayed in Django Admin
page.

To disable this supplement feature, set ``REGISTRATION_SUPPLEMENT_CLASS`` to
``None`` in your ``settings.py``.

Quick tutorial to create your own Registration Supplement
==========================================================================================

1.  Create new app named ``supplementtut`` with the command below::

        $ ./manage.py startapp supplementtut

2.  Create new registration supplement model in your ``models.py`` as::

        from django.db import models
        from registration.supplements import RegistrationSupplementBase

        class MyRegistrationSupplement(RegistrationSupplementBase):
            
            realname = models.CharField("Real name", max_length=100, help_text="Please fill your real name")
            age = models.IntegerField("Age")
            remarks = models.TextField("Remarks", blank=True)

            def __unicode__(self):
                # a summary of this supplement
                return "%s (%s)" % (self.realname, self.age)


3.  Add ``supplementtut`` to ``INSTALLED_APPS`` and set ``REGISTRATION_SUPPLEMENT_CLASS`` to
    ``"supplementtut.models.MyRegistrationSupplement`` in your ``settings.py``

4.  Done, execute ``syncdb`` and ``runserver`` to confirm your registration
    supplement is used correctly. See more documentation in
    :py:class:`registration.supplements.RegistrationSupplementBase`


