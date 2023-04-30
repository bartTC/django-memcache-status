from __future__ import annotations

import dataclasses
import logging

from django.conf import settings
from django.core.cache import caches

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class CacheStats:
    name: str
    address: str
    stats: any


def get_cache_stats() -> list[CacheStats]:
    """
    Returns a list of dictionaries of all cache servers and their stats,
    if they provide stats.
    """

    cache_stats: list[CacheStats] = []

    for name, _ in settings.CACHES.items():
        cache_backend = caches[name]

        # PyLibMCCache
        try:
            cache_backend_stats = cache_backend._cache.get_stats()
            for address, stats in cache_backend_stats:
                cache_stats.append(CacheStats(name, address, stats))
            continue
        except AttributeError:
            pass

        # PyMemcacheCache
        try:
            for address, client in cache_backend._cache.clients.items():
                cache_stats.append(CacheStats(name, address, client.stats()))
            continue
        except AttributeError:
            pass

        logger.info(
            'The memcached backend "%s" does not support or provide stats.',
            name,
        )
    return cache_stats
