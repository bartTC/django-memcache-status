from __future__ import unicode_literals

import logging
import six

from django import template
from django.conf import settings
from django.core.cache import get_cache

if get_cache.__module__.startswith('debug_toolbar'):
    from debug_toolbar.panels.cache import base_get_cache as get_cache

try:
    from django.core.cache import caches
except ImportError:
    from django.core.cache import get_cache as caches

if caches.__module__.startswith('debug_toolbar'):
    try:
        from debug_toolbar.panels.cache import base_get_cache as caches
    except ImportError:
        from debug_toolbar.panels.cache import get_cache as caches


get_cache = lambda cache_name: caches(cache_name) if hasattr(caches, '__call__') else caches[cache_name]
logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag(takes_context=True)
def get_cache_stats(context):
    """
    Reads the cache stats out of the memcached cache backend. Returns `None`
    if no cache stats supported.
    """
    cache_stats = []
    for cache_backend_nm, cache_backend_attrs in six.iteritems(settings.CACHES):
        try:
            cache_backend = get_cache(cache_backend_nm)
            this_backend_stats = cache_backend._cache.get_stats()
            if not this_backend_stats:
                logger.warning('The memcached backend "%s" does not support or '
                    'provide stats. (Or its no memcached, or its not running.)', cache_backend_nm)
            # returns list of (name, stats) tuples
            for server_name, server_stats in this_backend_stats:
                cache_stats.append(("%s: %s" % (
                    cache_backend_nm, server_name), server_stats))
        except AttributeError: # this backend probably doesn't support that
            logger.warning('The memcached backend "%s" does not support or '
                'provide stats.  (Or its no memcached, or its not running.)', cache_backend_nm)
    context['cache_stats'] = cache_stats
    return ''


class PrettyValue(object):
    """
    Helper class that reformats the value. Looks for a method named
    ``format_<key>_value`` and returns that value. Returns the value
    as is, if no format method is found.
    """

    def format(self, key, value):
        try:
            func = getattr(self, 'format_%s_value' % key.lower())
            return func(value)
        except AttributeError:
            return value

    def format_limit_maxbytes_value(self, value):
        return "%s (%s)" % (value, self.human_bytes(value))

    def format_bytes_read_value(self, value):
        return "%s (%s)" % (value, self.human_bytes(value))

    def format_bytes_written_value(self, value):
        return "%s (%s)" % (value, self.human_bytes(value))

    def format_uptime_value(self, value):
        return self.fract_timestamp(int(value))

    def format_time_value(self, value):
        from datetime import datetime
        return datetime.fromtimestamp(int(value)).strftime('%x %X')

    def fract_timestamp(self, s):
        years, s = divmod(s, 31556952)
        min, s = divmod(s, 60)
        h, min = divmod(min, 60)
        d, h = divmod(h, 24)
        return '%sy, %sd, %sh, %sm, %ss' % (years, d, h, min, s)

    def human_bytes(self, bytes):
        bytes = float(bytes)
        if bytes >= 1073741824:
            gigabytes = bytes / 1073741824
            size = '%.2fGB' % gigabytes
        elif bytes >= 1048576:
            megabytes = bytes / 1048576
            size = '%.2fMB' % megabytes
        elif bytes >= 1024:
            kilobytes = bytes / 1024
            size = '%.2fKB' % kilobytes
        else:
            size = '%.2fB' % bytes
        return size


@register.filter
def prettyname(name):
    return ' '.join([word.capitalize() for word in name.split('_')])


@register.filter
def prettyvalue(value, key):
    return PrettyValue().format(key, value)
