.. image:: https://img.shields.io/pypi/v/django-memcache-status.svg
    :target: https://pypi.org/project/django-memcache-status/

.. image:: https://travis-ci.org/bartTC/django-memcache-status.svg?branch=master
    :target: https://travis-ci.org/bartTC/django-memcache-status

.. image:: https://api.codacy.com/project/badge/Coverage/1d7d0306c4d14fb9817017d7d23237fe
    :target: https://www.codacy.com/app/bartTC/django-memcache-status

.. image:: https://api.codacy.com/project/badge/Grade/1d7d0306c4d14fb9817017d7d23237fe
    :target: https://www.codacy.com/app/bartTC/django-memcache-status

-----

======================
django-memcache-status
======================

This app displays the current load and some statistics for your memcached_
instances in the index view of your Django admin section.

Currently these memcached bindings are tested:

========================================================= ================================
Backend                                                   Support
========================================================= ================================
`python-memcached`_ with vanilla Django                   ✅ Works fine with >= v1.57
pylibmc with `django-pylibmc`_                            ✅ Works fine
pymemcache with `django-pymemcache`_                      ❎ Does not provide stats
========================================================= ================================

Other bindings may provide statistics too.

.. _memcached: http://www.danga.com/memcached/
.. _python-memcached: https://pypi.org/project/python-memcached/
.. _django-pylibmc: https://pypi.org/project/django-pylibmc/
.. _django-pymemcache: https://pypi.org/project/django-pymemcache/

Installation
============

First add ``memcache_status`` to your ``INSTALLED_APPS`` list.

::

    INSTALLED_APPS = [
        # ...
        'memcache_status',
    ]

Then you have two options:

1) The quickest way is to replace your Django Admin index page with the one
   provided by django-memcache-status. This will show the memcache stats in the
   top left column. This was the regular behavior of django-memcache-status
   prior to version 2.0.

   Place this in any ``admin.py`` file of your project::

    from django.contrib import admin
    admin.site.index_template = 'memcache_status/admin_index.html'


2) If you need to manually place the stats, simply add the CSS file and include
   the memcache-status template anywhere you like::

    <link rel="stylesheet" href="{% static "memcache_status.css" %}"/>
    {% include "memcache_status/memcache_status.html" %}


Local Development
=================

Install the package using Pipenv and run the tests::

    $ pipenv install --dev
    $ pipenv run test

You can test against a matrix of Python and Django versions using tox::

    $ tox

Once run you will see a coverage report in `/tmp/coverage_report/django-memcache-status`.

You can run a local runserver with the test application to see the
admin::

    $ pipenv run django-admin.py migrate
    $ pipenv run django-admin.py createsuperuser
    $ pipenv run django-admin.py runserver

To test a specific cache backend define it in the env variable::

    $ TEST_CACHE_BACKEND=django-pylibmc pipenv run django-admin.py runserver


.. note:: If you're testing pylibmc on OS X and you get an error like
    ``'libmemcached/memcached.h' file not found``, install pylibmc manually,
    then run the installation again::

    $ brew install libmemcached
    $ pipenv run pip install pylibmc --install-option="--with-libmemcached=/usr/local/Cellar/libmemcached/1.0.18_2/"
    $ pipenv install --dev

----

Changelog
=========

**v2.2 (2020-02-05):**

- Compatibility and tests for Django 2.2 and 3.0, and Python 3.8.
- Use pytest for testing. 

**v2.1 (2019-03-21):**

- Removed some deprecated django-debug-toolbar and pre-Django 1.11
  related workarounds.
- More comprehensive unittests across all backends and it's relation
  with django-debug-toolbar.

**v2.0 (2019-03-16):**

- Compatibility and tests for Django 1.11 → 2.1 and Python 2.7 → 3.7.
- Full code cleanup and update to latest standards.
- Tested against a variety of memcache bindings.
- Pipenv support for local development and testing.
- *[Backwards Incompatible]* memcache-status no longer automatically overwrites
  the admin index template to add the stats. Instead you have the option to
  either  manually display the stats anywhere you like using a template include,
  or use the contributed memcache-status admin index page that overwrites the
  vanilla Django template and adds statistics to the top left admin index page.
  This was the regular behavior of django-memcache-status prior to version 2.0.

**v1.3 (2016-10-13):**

- Django 1.10 compatibility and test integration. Python 3 compatibility.

**v1.2 (2009-11-06):**

- Unittests, General code cleanup to support Django 1.8+ features such as
- AppConfig, Django-Debugtoolbar support, Python3 Support, Compatibility tests
- with latest supported Django versions (currently Django 1.8 and 1.9) but the
- package is likely working with Django 1.4+.

**v1.1 (2009-06-29):**

- Added support for Django's multiple cache backend setting. Kudos to Luke
  Granger-Brown for the implementation.
- This version is compatible with Django v1.3 and up.

**v1.0 (2009-04-30):**

- Initial Release.
- This version is compatible up to Django v1.2.

----

Screenshots
===========

.. image:: https://user-images.githubusercontent.com/1896/54476030-f0dd3080-47f8-11e9-8399-b11f3bf15ebc.png
   :target: https://user-images.githubusercontent.com/1896/54476030-f0dd3080-47f8-11e9-8399-b11f3bf15ebc.png
   :align: left
   :height: 200px

.. image:: https://user-images.githubusercontent.com/1896/54476031-f470b780-47f8-11e9-842f-95d880563a53.png
   :target: https://user-images.githubusercontent.com/1896/54476031-f470b780-47f8-11e9-842f-95d880563a53.png
   :height: 300px