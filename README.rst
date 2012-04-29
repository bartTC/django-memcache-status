======================
django-memcache-status
======================

This app displays the current load and some statistics for your memcached_
instances in the index view of your Django admin section.

Installation
============

Put ``memcache_status`` in your ``INSTALLED_APPS``.

That's all. Only admin-users with ``superuser`` permission can see these stats.

Screenshots
===========

.. image:: https://github.com/downloads/bartTC/django-memcache-status/memcache_status_1.png

Overview in your Admin index view. Allows multiple memcached instances.

.. image:: https://github.com/downloads/bartTC/django-memcache-status/memcache_status_2.png

Details if you click on a instance

.. _memcached: http://www.danga.com/memcached/


Changelog
=========

**v1.1:**
    Added support for Django's multiple cache backend setting. Kudos to Luke
    Granger-Brown for the implementation.

    This version is compatible with Django v1.3 and up.

**v1.0:**
    Initial Release.

    This version is compatible up to Django v1.2.
