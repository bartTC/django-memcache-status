======================
django-memcache-status
======================

This app displays the current load and some statistics for your memcached_
instances in the index view of your Django admin section. It's tested with
*Django 1.0.2* and *Django 1.1*.

Installation
============

Put ``memcache_status`` in your ``INSTALLED_APPS``.

That's all. Only admin-users with ``superuser`` permission can see these stats.

Screenshots
===========

.. image:: http://cloud.github.com/downloads/bartTC/django-memcache-status/memcache_status_1.png

Overview in your Admin index view. Allows multiple memcached instances.

.. image:: http://cloud.github.com/downloads/bartTC/django-memcache-status/memcache_status_2.png

Details if you click on a instance

.. _memcached: http://www.danga.com/memcached/