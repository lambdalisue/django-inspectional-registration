This is a `django-registration`_ derivered app which add inspection feature before activation.

A lot of code is copied from django-registration and this django-inspectional-registration is still developing

Difference
====================

Normal django-registration
----------------------------------------------------

1.  User register the Web site with username, email and password
2.  User got activation mail
3.  User access the URL and activated. User can now login with the previous
    username and password

django-inspectional-registration
----------------------------------------------------------------

1.  User register the Web site with username and email. Not with password
2.  Inspector check the registration and accept or reject the registration
3.  If inspector accept the registration, the user get acception email and
    activation url
4.  If inspector reject the registration, the user get rejection email
