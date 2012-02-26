# vim: set fileencoding=utf8:
from setuptools import setup, find_packages

version = '0.2.3'

def read(filename):
    import os.path
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name="django-inspectional-registration",
    version=version,
    description = "Django Registration App which required Inspection before activation",
    long_description=read('README.rst'),
    classifiers = [
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',

    ],
    keywords = "django app registration inspection",
    author = "Alisue",
    author_email = "lambdalisue@hashnote.net",
    url=r"https://github.com/lambdalisue/django-inspectional-registration",
    download_url = r"https://github.com/lambdalisue/django-inspectional-registration/tarball/master",
    license = 'MIT',
    packages = find_packages(),
    include_package_data = True,
    install_requires=[
        'django>=1.3',
        'distribute',
        'setuptools-git',
    ],
    test_suite='runtests.runtests',
    tests_require=[
        'PyYAML',
    ],
)
