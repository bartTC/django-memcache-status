#!/usr/bin/env python
from sys import exit

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errno = tox.cmdline(self.test_args)
        exit(errno)

setup(
    name='django-memcache-status',
    version='1.3',
    description='A django application that displays the load and some other '
                'statistics about your memcached instances in the admin.',
    long_description=open('README.rst').read(),
    author='Martin Mahner',
    author_email='martin@mahner.org',
    url='http://github.com/bartTC/django-memcache-status',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
    install_requires=[
        'six',
        'django>=1.8',
        'python-memcached>=1.57',
    ],
    tests_require=[
        'tox>=1.6.1',
    ],
    cmdclass={
        'test': Tox
    },
)
