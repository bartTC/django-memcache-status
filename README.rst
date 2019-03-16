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

- `python-memcached`_ (Version >=1.57) with vanilla Django: Works fine
- pylibmc with `django-pylibmc`_: Works fine
- pymemcache with `django-pymemcache`_: Does not provide stats

Other bindings may provide statistics too.

.. _memcached: http://www.danga.com/memcached/
.. _python-memcached: https://pypi.org/project/python-memcached/
.. _django-pylibmc: https://pypi.org/project/django-pylibmc/
.. _django-pymemcache: https://pypi.org/project/django-pymemcache/

Installation
============

Put ``memcache_status`` in your ``INSTALLED_APPS``.

That's all. Only admin-users with ``is_superuser`` permission can see these
stats.

Screenshots
===========

.. image:: https://user-images.githubusercontent.com/1896/54476030-f0dd3080-47f8-11e9-8399-b11f3bf15ebc.png

Overview in your Admin index view. Allows multiple memcached instances.

.. image:: https://user-images.githubusercontent.com/1896/54476031-f470b780-47f8-11e9-842f-95d880563a53.png

Details if you click on a instance

Local Development
=================

Install the package using Pipenv and run the tests::

    $ pipenv install --dev
    $ pipenv run test

You can test against a matrix of Python and Django versions using tox::

    $ tox

You can run a local runserver with the test application to see the
admin::

    $ pipenv run django-admin.py migrate
    $ pipenv run django-admin.py createsuperuser
    $ pipenv run django-admin.py runserver

To test a specific cache backend define it in the env variable::

    $ TEST_CACHE_BACKEND=django-pylibmc pipenv run django-admin.py runserver

Changelog
=========

**v2.0 (2019-03-16):**

- Compatibility and tests for Django 1.11 ⇥ 2.1 and Python 2.7 ⇥ 3.7.
- Full code cleanup and update to latest standards.
- Visual and CSS overhaul.
- Multiple cache backends tested.
- Pipenv support for local development and testing.

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
