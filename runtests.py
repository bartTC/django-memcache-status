#!/usr/bin/env python
import os
import sys
from django.conf import settings

SETTINGS = {
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        },
    },
    'INSTALLED_APPS': [
        'memcache_status',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
    ],
    'ROOT_URLCONF': 'memcache_status.tests.urls',
    'CACHES': {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    },
    'MIDDLEWARE_CLASSES': [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
    ],
    'TEMPLATES': [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.request',
                    'django.template.context_processors.i18n',
                    'django.contrib.auth.context_processors.auth',
                ],
            },
        },
    ]
}


if os.getenv('TEST_WITH_DEBUGTOOLBAR', False) == 'on':
    sys.stdout.write('Testing with django-debug-toolbar support.\n')
    SETTINGS['INSTALLED_APPS'].insert(0, 'debug_toolbar')
    SETTINGS['MIDDLEWARE_CLASSES'].append('debug_toolbar.middleware.DebugToolbarMiddleware')
    SETTINGS['INTERNAL_IPS'] = ['127.0.0.1']


def runtests(*test_args):
    # Setup settings
    if not settings.configured:
        settings.configure(**SETTINGS)

    # New Django 1.7 app registry setup
    try:
        from django import setup
        setup()
    except ImportError:
        pass

    # New Django 1.8 test runner
    try:
        from django.test.runner import DiscoverRunner as TestRunner
    except ImportError:
        from django.test.simple import DjangoTestSuiteRunner as TestRunner

    test_runner = TestRunner(verbosity=1)
    failures = test_runner.run_tests(['memcache_status'])
    if failures:
        sys.exit(failures)

if __name__ == '__main__':
    runtests(*sys.argv[1:])
