import logging

from django.conf import settings
from django.core.cache import caches

logger = logging.getLogger(__name__)


def get_cache_stats() -> list:
    """
    Returns a list of dictionaries of all cache servers and their stats,
    if they provide stats.
    """
    cache_stats = []
    for name, _ in settings.CACHES.items():
        cache_backend = caches[name]

        try:
            cache_backend_stats = cache_backend._cache.get_stats()
        except AttributeError:  # this backend doesn't provide stats
            try:
                cache_backend_stats = cache_backend._cache.stats()
            except AttributeError:
                logger.info(
                    'The memcached backend "%s" does not support or provide stats.',
                    name,
                )
                continue

        for address, stats in cache_backend_stats:
            cache_stats.append(
                {"name": name, "address": address, "stats": stats},
            )
    return cache_stats
