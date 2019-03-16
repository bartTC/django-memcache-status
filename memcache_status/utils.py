from __future__ import unicode_literals

import logging

import six
from django.conf import settings

try:
    from django.core.cache import caches
except ImportError:
    from django.core.cache import get_cache as caches

if caches.__module__.startswith('debug_toolbar'):
    try:
        from debug_toolbar.panels.cache import base_get_cache as caches
    except ImportError:
        from debug_toolbar.panels.cache import get_cache as caches


get_cache = (
    lambda cache_name: caches(cache_name)
    if hasattr(caches, '__call__')
    else caches[cache_name]
)

logger = logging.getLogger(__name__)


def get_cache_stats():
    """
    Returns a list of dictionaries of all cache servers and their stats,
    if they provide stats.
    """
    cache_stats = []
    for name, _ in six.iteritems(settings.CACHES):
        try:
            cache_backend = get_cache(name)
            cache_backend_stats = cache_backend._cache.get_stats()
        except AttributeError:  # this backend doesn't provide stats
            logger.info(
                'The memcached backend "{0}" does not support or '
                'provide stats.'.format(name)
            )
            continue

        for address, stats in cache_backend_stats:
            cache_stats.append(
                {'name': name, 'address': address, 'stats': stats}
            )
    return cache_stats
