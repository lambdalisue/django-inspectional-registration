# vim: set fileencoding=utf-8 :
from setuptools import setup, find_packages

version = '0.2.18'

def read(filename):
    import os
    BASE_DIR = os.path.dirname(__file__)
    filename = os.path.join(BASE_DIR, filename)
    with open(filename, 'r') as fi:
        return fi.read()

def readlist(filename):
    rows = read(filename).split("\n")
    rows = [x.strip() for x in rows]
    rows = filter(lambda x: x, rows)
    return rows

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
    zip_safe=False,
    install_requires=readlist('requirements.txt'),
    test_suite='runtests.runtests',
    tests_require=readlist('requirements-test.txt'),
)
