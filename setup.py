# coding=utf-8
import sys
import os
from setuptools import setup, find_packages, Command
from setuptools.command.sdist import sdist as original_sdist

NAME = 'django-inspectional-registration'
VERSION = '0.4.3'


class compile_docs(Command):
    description = ("re-compile documentations")
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        compile_docs.compile_docs()

    @classmethod
    def compile_docs(cls):
        """
        Compile '.rst' files into '.html' files via Sphinx.
        """
        original_cwd = os.getcwd()
        BASE = os.path.abspath(os.path.dirname(__file__))
        root = os.path.join(BASE, 'docs')
        os.chdir(root)
        os.system('make html')
        os.system('xdg-open _build/html/index.html')
        os.chdir(original_cwd)
        return True


class compile_messages(Command):
    description = ("re-compile local message files ('.po' to '.mo'). "
                   "it require django-admin.py")
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        compile_messages.compile_messages()

    @classmethod
    def compile_messages(cls):
        """
        Compile '.po' into '.mo' via 'django-admin.py' thus the function
        require the django to be installed.

        It return True when the process successfully end, otherwise it print
        error messages and return False.

        https://docs.djangoproject.com/en/dev/ref/django-admin/#compilemessages
        """
        try:
            import django
        except ImportError:
            print('####################################################\n'
                  'Django is not installed.\nIt will not be possible to '
                  'compile the locale files during installation of '
                  'django-inspectional-registration.\nPlease, install '
                  'Django first. Done so, install the django-registration'
                  '-inspectional\n'
                  '####################################################\n')
            return False
        else:
            original_cwd = os.getcwd()
            BASE = os.path.abspath(os.path.dirname(__file__))
            root = os.path.join(BASE, 'src/registration')
            os.chdir(root)
            os.system('django-admin.py compilemessages')
            os.chdir(original_cwd)
            return True


class sdist(original_sdist):
    """
    Run 'sdist' command but make sure that the message files are latest by
    running 'compile_messages' before 'sdist'
    """
    def run(self):
        compile_messages.compile_messages()
        original_sdist.run(self)


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
    name=NAME,
    version=VERSION,
    description=("Django registration app which required inspection step "
                 "before activation"),
    long_description = read('README.rst'),
    classifiers = (
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
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
    package_data = {
        '': ['README.rst',
             'requirements.txt',
             'requirements-test.txt',
             'requirements-docs.txt'],
    },
    zip_safe=True,
    install_requires=readlist('requirements.txt'),
    test_suite='runtests.run_tests',
    tests_require=readlist('requirements-test.txt'),
    cmdclass={
        'compile_messages': compile_messages,
        'compile_docs': compile_docs,
        'sdist': sdist,
    },
    **extra
)
