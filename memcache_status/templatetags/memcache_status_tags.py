from django import template
from django.conf import settings
from django.core.cache import get_cache
from django.template.base import TemplateSyntaxError
from django.template.defaulttags import WidthRatioNode

if get_cache.__module__.startswith('debug_toolbar'):
    from debug_toolbar.panels.cache import base_get_cache as get_cache

register = template.Library()


class SafeWidthRatioNode(WidthRatioNode):
    """
    Custom ``WidthRatioNode`` template tag which stops when percentage is over
    100% to avoid overdrawing graphs.
    """
    def render(self, context):
        ratio = super(SafeWidthRatioNode, self).render(context)

        if int(ratio) > 100:
            ratio = '100'

        return ratio


@register.tag
def safewidthratio(parser, token):
    """
    For creating bar charts and such, this tag calculates the ratio of a given
    value to a maximum value, and then applies that ratio to a constant.

    For example::

        <img src='bar.gif' height='10' width='{% widthratio this_value max_value max_width %}' />

    If ``this_value`` is 175, ``max_value`` is 200, and ``max_width`` is 100,
    the image in the above example will be 88 pixels wide
    (because 175/200 = .875; .875 * 100 = 87.5 which is rounded up to 88).
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise TemplateSyntaxError("widthratio takes three arguments")
    tag, this_value_expr, max_value_expr, max_width = bits

    return SafeWidthRatioNode(parser.compile_filter(this_value_expr),
                              parser.compile_filter(max_value_expr),
                              parser.compile_filter(max_width))


class CacheStats(template.Node):
    """
    Reads the cache stats out of the memcached cache backend. Returns `None`
    if no cache stats supported.
    """
    def render(self, context):
        cache_stats = []
        for cache_backend_nm, cache_backend_attrs in settings.CACHES.iteritems():
            try:
                cache_backend = get_cache(cache_backend_nm)
                this_backend_stats = cache_backend._cache.get_stats()
                # returns list of (name, stats) tuples
                for server_name, server_stats in this_backend_stats:
                    cache_stats.append(("%s: %s" % (
                        cache_backend_nm, server_name), server_stats))
            except AttributeError: # this backend probably doesn't support that
                continue
        context['cache_stats'] = cache_stats
        return ''

@register.tag
def get_cache_stats(parser, token):
    return CacheStats()

@register.filter
def prettyname(name):
    return ' '.join([word.capitalize() for word in name.split('_')])

@register.filter
def prettyvalue(value, key):
    return PrettyValue().format(key, value)

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
