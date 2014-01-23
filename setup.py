# coding=utf-8
import sys
from setuptools import setup, find_packages

NAME = 'django-inspectional-registration'
VERSION = '0.3.0'

def read(filename):
    import os
    BASE_DIR = os.path.dirname(__file__)
    filename = os.path.join(BASE_DIR, filename)
    with open(filename, 'r') as fi:
        return fi.read()

def readlist(filename):
    rows = read(filename).split("\n")
    rows = [x.strip() for x in rows if x.strip()]
    return list(rows)

# if we are running on python 3, enable 2to3 and
# let it use the custom fixers from the custom_fixers
# package.
extra = {}
if sys.version_info >= (3, 0):
    extra.update(
        use_2to3=True,
    )

setup(
    name = NAME,
    version = VERSION,
    description = ("Django registration app which required inspection step "
                   "before activation"),
    long_description = read('README.rst'),
    classifiers = (
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ),
    keywords = "django app registration inspection",
    author = 'Alisue',
    author_email = 'lambdalisue@hashnote.net',
    url = 'https://github.com/lambdalisue/%s' % NAME,
    download_url = 'https://github.com/lambdalisue/%s/tarball/master' % NAME,
    license = 'MIT',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data = True,
    exclude_package_data = {'': ['README.rst']},
    zip_safe=True,
    install_requires=readlist('requirements.txt'),
    test_suite='runtests.runtests',
    tests_require=readlist('requirements-test.txt'),
    **extra
)
