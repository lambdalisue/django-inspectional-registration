#!/usr/bin/env python
# coding: utf-8
"""
Run Django Test with Python setuptools test command


REFERENCE:
    http://gremu.net/blog/2010/enable-setuppy-test-your-django-apps/

"""
import os
import sys

def parse_args():
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('--where', default=None)
    opts, args = parser.parse_args()
    return opts.where

def run_tests(base_dir=None, verbosity=1, interactive=False):
    base_dir = base_dir or os.path.dirname(__file__)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    sys.path.insert(0, os.path.join(base_dir, 'src'))
    sys.path.insert(0, os.path.join(base_dir, 'tests'))

    from django.conf import settings
    from django.test.utils import get_runner
    """Run Django Test"""
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=verbosity,
                             interactive=interactive, failfast=False)

    import django
    if django.VERSION >= (1, 6):
        app_tests = [
            'registration',
            'registration.contrib.notification',     # registration.contrib.notification
            'registration.contrib.autologin',        # registration.contrib.autologin
        ]
    else:
        app_tests = [
            'registration',
            'notification',     # registration.contrib.notification
            'autologin',        # registration.contrib.autologin
        ]
    failures = test_runner.run_tests(app_tests)
    sys.exit(bool(failures))

if __name__ == '__main__':
    base_dir = parse_args()
    run_tests(base_dir)

