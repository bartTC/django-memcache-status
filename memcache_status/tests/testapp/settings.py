import os
import sys

DEBUG = True

TESTAPP_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'testsecretkey'

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(TESTAPP_DIR, 'testdb.sqlite'),
    }
}

# Cache backends to test based on ENV variabe below.
CACHE_BACKENDS_TO_TEST = {
    'python-memcached': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',

        # Flag only used for the unittests. It indicates whether its expected
        # that this backend provides stats or not.
        'TEST_PROVIDES_STATS': True,
    },

    'django-pylibmc': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',

        # Flag only used for the unittests. It indicates whether its expected
        # that this backend provides stats or not.
        'TEST_PROVIDES_STATS': True,
    },

    'django-pymemcache': {
        'BACKEND': 'djpymemcache.backend.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',

        # Flag only used for the unittests. It indicates whether its expected
        # that this backend provides stats or not.
        'TEST_PROVIDES_STATS': False,
    },
}

CACHE_LABEL = os.environ.get('TEST_CACHE_BACKEND', 'python-memcached')
if CACHE_LABEL not in CACHE_BACKENDS_TO_TEST:
    sys.stderr.write('\nCache backend % is not defined in the settings\n' % CACHE_LABEL)
    exit(1)


sys.stdout.write('Testing cache backend: %s\n' % CACHE_LABEL)
CACHES = {'default': CACHE_BACKENDS_TO_TEST[CACHE_LABEL]}


STATIC_ROOT = os.path.join(TESTAPP_DIR, '.static')
MEDIA_ROOT = os.path.join(TESTAPP_DIR, '.uploads')

STATIC_URL = '/static/'
MEDIA_URL = '/uploads/'

ROOT_URLCONF = 'memcache_status.tests.testapp.urls'

INSTALLED_APPS = [
    'memcache_status',
    'memcache_status.tests.testapp',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    }
]

if os.getenv('TEST_WITH_DEBUGTOOLBAR', False) == 'on':
    sys.stdout.write('Testing with django-debug-toolbar support.\n')
    INSTALLED_APPS.insert(0, 'debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

    # Make sure debug toolbar is always visible, even in Unittests.
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: True
    }
