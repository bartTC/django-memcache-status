#!/usr/bin/env python
import sys
from django.conf import settings
from django.core.management import execute_from_command_line

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        INSTALLED_APPS=(
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'memcache_status',
        ),
        ROOT_URLCONF=None,
        SECRET_KEY='foobar',
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
                'LOCATION': '127.0.0.1:11211',
            }
        }
    )


def runtests():
    argv = sys.argv[:1] + ['test'] + sys.argv[1:] + ['memcache_status']
    execute_from_command_line(argv)


if __name__ == '__main__':
    runtests()